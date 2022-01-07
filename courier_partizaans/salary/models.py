from math import fabs

from django.db import models


# Create your models here.
from courier.models import Courier


class TripIncome(models.Model):
    """

    Trip income model for saving income for each trip
    """
    courier = models.ForeignKey(Courier,on_delete=models.CASCADE)
    income = models.PositiveIntegerField()
    date = models.DateField(auto_created=True)

    def save(self,*args,**kwargs):
        """
        overwrite save method of Trip income model to save automatically
        daily income when a trip income saved
        """
        instance = super(TripIncome,self).save(*args,**kwargs)
        try:
            daily_income = DailyIncome.objects.get(courier=self.courier,date=self.date)
            daily_income.amount += self.income
            daily_income.save()

        except DailyIncome.DoesNotExist:
            DailyIncome.objects.create(courier=self.courier,date=self.date,amount=self.income)

        return instance

    def __str__(self):
        return f'Trip income {self.courier.name} date:{self.date}'


class IncreaseIncome(models.Model):

    """
    Increase income model for save how much should be increase for
    courier's daily trip
    """
    courier = models.OneToOneField(Courier,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    description = models.CharField(max_length=200,default=None)

    def __str__(self):
        return f'Increase amount:{self.amount},{self.courier.name} , description:{self.description}'

class DecreaseIncome(models.Model):
    """
    Decrease income model for save how much should be decrease for
    courier's daily trip
    """
    courier = models.OneToOneField(Courier, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    description = models.CharField(max_length=200,default=None)


    def __str__(self):
        return f'Decrease amount:{self.amount},{self.courier.name} , description:{self.description}'

class DailyIncome(models.Model):

    """
    Daily income model for save all trip's income for each day
    """

    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    date = models.DateField(auto_created=True)


    def save(self,*args,**kwargs):

        """
        overwrite save method of Daily income model for save week income
        automatically for each day and if increase or decrease for
        courier was set it will be apply

        """
        instance = super(DailyIncome,self).save(*args,**kwargs)
        try:
            increase = IncreaseIncome.objects.get(courier=self.courier)
            self.amount += increase.amount

        except IncreaseIncome.DoesNotExist:
            pass
        try:
            decrease = DecreaseIncome.objects.get(courier=self.courier)
            self.amount -= decrease.amount

            if self.amount <= 0:
                self.amount = 0
        except DecreaseIncome.DoesNotExist:
            pass

        if self.date.isoweekday() == 6 :
            try:
                week_income = WeekIncome.objects.get(courier=self.courier,saturday=self.date)
                week_income.income += self.amount
                week_income.save()
            except WeekIncome.DoesNotExist:
                week_income = WeekIncome.objects.create(courier=self.courier,saturday=self.date)
                week_income.income += self.amount
                week_income.save()
        else:
            week_incomes = WeekIncome.objects.filter(saturday__month=self.date.month,saturday__year=self.date.year)
            for week_income in week_incomes:
                if fabs(week_income.saturday.day - self.date.day) <= 7 :
                    week_income.income += self.amount
                    week_income.save()
                    break

        return instance


    def __str__(self):
        return f'Daily income :{self.amount},{self.courier.name}, date:{self.date}'




class WeekIncome(models.Model):


    """
    Week income model for save all daily income in each week that
    starts with saturday
    """
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    saturday = models.DateField()
    income = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Week income:{self.income},{self.courier.name} , saturday:{self.saturday}'