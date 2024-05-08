from django.contrib import admin
from .models import DrinksCategory, Drinks, Booking, Employee, Menu

# Register your models here.
admin.site.register(DrinksCategory)
admin.site.register(Drinks)
admin.site.register(Booking)
admin.site.register(Employee)
admin.site.register(Menu)
