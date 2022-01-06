from django.db import models


# Create your models here.

class TripIncome(models.Model):
    courier = models.ForeignKey(Courier,on_delete=models.CASCADE)
    income = models.PositiveIntegerField()
    date = models.DateField(auto_created=True)

    def save(self,*args,**kwargs):
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
    pass

class DecreaseIncome(models.Model):
    pass

class DailyIncome(models.Model):
    pass

class WeekIncome(models.Model):
    pass

