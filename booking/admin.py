from django.contrib import admin
from rangefilter.filters import DateRangeFilter

from booking.models import Booking, Payment


class PaymentInline(admin.TabularInline):
    model = Payment


class BookingAdmin(admin.ModelAdmin):
    list_filter = (('created_dt', DateRangeFilter), 'program', 'status')
    list_display = ('id', 'program', 'status', 'customer', 'modified_dt')
    ordering = ('-id',)
    inlines = [
        PaymentInline,
    ]


# class PaymentAdmin(admin.ModelAdmin):
#     list_filter = (('modified_dt', DateRangeFilter), 'refund_rate')
#     list_display = ('id', 'refund_rate', 'amount', 'modified_dt')
#     ordering = ('-id',)


admin.site.register(Booking, BookingAdmin)
admin.site.register(Payment) # , PaymentAdmin)
