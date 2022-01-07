from django.test import TestCase
from datetime import datetime

# Create your tests here.
from courier.models import Courier
from salary.models import TripIncome, DailyIncome, IncreaseIncome, DecreaseIncome, WeekIncome


class DailyIncomeTest(TestCase):

    def setUp(self):

        self.courier = Courier.objects.create(name='Ali')

    def test_DailyIncome(self):

        TripIncome.objects.create(courier=self.courier, income=100, date=datetime(2022, 1, 8))
        daily_income = DailyIncome.objects.all()
        self.assertEqual(daily_income.first().amount,100)
        self.assertEqual(len(daily_income),1)

        TripIncome.objects.create(courier=self.courier, income=200, date=datetime(2022, 1, 8))
        daily_income = DailyIncome.objects.all()
        self.assertEqual(daily_income.first().amount, 300)
        self.assertEqual(len(daily_income), 1)

        TripIncome.objects.create(courier=self.courier, income=200, date=datetime(2022, 1, 9))
        daily_income = DailyIncome.objects.all()
        self.assertEqual(daily_income.first().amount, 300)
        self.assertEqual(daily_income.last().amount,200)
        self.assertEqual(len(daily_income), 2)


        IncreaseIncome.objects.create(courier=self.courier,amount=10,description='something...')
        TripIncome.objects.create(courier=self.courier, income=200, date=datetime(2022, 1, 10))
        daily_income = DailyIncome.objects.all()
        self.assertEqual(len(daily_income), 3)
        self.assertEqual(WeekIncome.objects.first().income,810)



