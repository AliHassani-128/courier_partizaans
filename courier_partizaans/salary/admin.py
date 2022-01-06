from django.contrib import admin

# Register your models here.
from salary.models import TripIncome, IncreaseIncome, DecreaseIncome, DailyIncome, WeekIncome

admin.site.register(TripIncome)
admin.site.register(IncreaseIncome)
admin.site.register(DecreaseIncome)
admin.site.register(DailyIncome)
admin.site.register(WeekIncome)