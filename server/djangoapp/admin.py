from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.TabularInline):
    model = CarModel

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

admin.site.register(CarMake, CarMakeAdmin)

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['car_make', 'name', 'dealer_id', 'car_type', 'year']
    list_filter = ['car_make', 'car_type', 'year']
    search_fields = ['name', 'dealer_id']

# from .models import related models


# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
