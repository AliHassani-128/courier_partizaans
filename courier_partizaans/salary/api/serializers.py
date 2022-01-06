from rest_framework import serializers

from salary.models import WeekIncome


class WeekIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekIncome
        depth = 2
        fields = '__all__'
