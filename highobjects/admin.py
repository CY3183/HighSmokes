from django.contrib import admin
from .models import EventsRawMode


@admin.register(EventsRawMode)    ## 高空抛物
class EventsRawModeAdmin(admin.ModelAdmin):
    list_display = ('dateTime', "deviceID", 'eventType', 'macAddress', 'eventDescription')
    search_fields = ('deviceID',)
    list_filter = ('dateTime', 'eventType')