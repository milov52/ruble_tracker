from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Rate, Currency, UserCurrencyTracking, CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],
            password=validated_data['password']
        )
        return user


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('char_code', 'name')


class RatesSerializer(serializers.ModelSerializer):
    charcode = serializers.CharField(source="currency.char_code")
    currency_status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rate
        fields = ('id', 'date', 'charcode', 'value', 'currency_status')

    def get_currency_status(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            user_currencies = UserCurrencyTracking.objects.filter(user_id=user, currency=obj.currency)
            currency_pz = user_currencies.first().pz
            currency_pz = Decimal(currency_pz.replace(',', '.'))

            if obj.value > currency_pz:
                return "Котировка превысила ПЗ"
            elif obj.value < currency_pz:
                return "Котировка ниже чем ПЗ"
            return "Котировка равна ПЗ"

        return None


class UserCurrencySerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserCurrencyTracking
        fields = ('currency', 'threshold', 'user_id')


class CurrencyAnalyticsSerializer(serializers.ModelSerializer):
    charcode = serializers.CharField(source="currency.char_code")
    is_threshold_exceeded = serializers.SerializerMethodField(read_only=True)
    threshold_match_type = serializers.SerializerMethodField(read_only=True)
    is_max_value = serializers.SerializerMethodField()
    is_min_value = serializers.SerializerMethodField()
    percentage_ratio = serializers.SerializerMethodField()

    class Meta:
        model = Rate
        fields = ('id',
                  'date',
                  'charcode',
                  'value',
                  'is_threshold_exceeded',
                  'threshold_match_type',
                  'is_max_value',
                  'is_min_value',
                  'percentage_ratio')

    def get_is_threshold_exceeded(self, obj):
        request = self.context.get('request')
        threshold = request.query_params.get('threshold')
        return threshold and Decimal(threshold) < Decimal(obj.value)

    def get_threshold_match_type(self, obj):
        request = self.context.get('request')
        threshold = request.query_params.get('threshold')
        if not threshold:
            return None
        if Decimal(threshold) < Decimal(obj.value):
            return "less"
        elif Decimal(threshold) == Decimal(obj.value):
            return "equal"
        else:
            return "exceeded"

    def get_is_max_value(self, obj):
        queryset = self.instance
        max_value = max(queryset, key=lambda item: item.value).value
        return obj.value == max_value

    def get_is_min_value(self, obj):
        queryset = self.instance
        min_value = min(queryset, key=lambda item: item.value).value
        return obj.value == min_value

    def get_percentage_ratio(self, obj):
        request = self.context.get('request')
        threshold = request.query_params.get('threshold')

        if not threshold:
            return None

        ratio = Decimal(obj.value) / Decimal(threshold) * 100
        return f'{ratio:.2f}%'