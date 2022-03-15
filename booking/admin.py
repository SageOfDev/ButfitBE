from django.contrib import admin

from booking.models import Booking, Payment

admin.site.register(Booking)
admin.site.register(Payment)