from django.contrib import admin

from program.models import Program


class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'start_time')


admin.site.register(Program, ProgramAdmin)
