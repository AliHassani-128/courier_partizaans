from rest_framework import generics

from salary.api.serializers import WeekIncomeSerializer
from salary.models import WeekIncome


class WeekIncomeView(generics.ListAPIView):
    model = WeekIncome
    serializer_class = WeekIncomeSerializer
    def get_queryset(self):
        queryset = WeekIncome.objects.all()
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')
        if from_date:
            queryset = queryset.filter(saturday=from_date)
        if to_date:
            queryset = queryset.filter(saturday=to_date)
        return queryset