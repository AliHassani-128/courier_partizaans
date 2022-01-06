from django.urls import path

from salary.api.views import WeekIncomeView

urlpatterns = [
    path('week_income/',WeekIncomeView.as_view(),name='WeekIncomeView'),
]