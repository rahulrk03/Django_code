from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import PhoneToken,Country,City


class PhoneTokenAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'otp', 'timestamp', 'attempts', 'used')
    search_fields = ('phone_number', )
    list_filter = ('timestamp', 'attempts', 'used')
    readonly_fields = ('phone_number', 'otp', 'timestamp', 'attempts')


admin.site.register(PhoneToken, PhoneTokenAdmin)

admin.site.register(Country)

admin.site.register(City)
