from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name='register'),
    path("login/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("login/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("rates/", views.RatesViewSet.as_view({'get': 'list'})),
    path("currency/user_currency/", views.UserCurrencyViewSet.as_view({'post': 'create'})),
    path("currency/add/", views.AddCurrencyViewSet.as_view()),
    path("currency/<int:id>/analytics/", views.CurrencyAnalyticsViewSet.as_view({'get': 'list'})),
]
