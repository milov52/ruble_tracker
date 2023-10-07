from django.db.models import F
from rest_framework import viewsets, status, generics, filters, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Rate, UserCurrencyTracking
from .serializers import RatesSerializer, UserCurrencySerializer, UserSerializer, CurrencyAnalyticsSerializer

from ruble_tracker.tasks import update_rates

class RegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserCurrencyViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = UserCurrencyTracking.objects.all()
    serializer_class = UserCurrencySerializer
    permission_classes = (IsAuthenticated,)


class CurrencyAnalyticsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CurrencyAnalyticsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        return Rate.objects.filter(
            currency=self.kwargs.get("id"),
            date__gte=date_from,
            date__lte=date_to
        )


class RatesViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RatesSerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            users_currencies = UserCurrencyTracking.objects.filter(
                user_id=self.request.user.id,
                currency=F('currency')
            )

            currency_ids = [uc.currency.id for uc in users_currencies]
            return Rate.objects.filter(currency__in=currency_ids)
        return Rate.objects.all()

class AddCurrencyViewSet(APIView):

    def get(self, request):
        update_rates()
        return Response({"status": "ok"})
