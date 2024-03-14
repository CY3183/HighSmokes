from django.contrib import admin
from .models import EventsRawMode


@admin.register(EventsRawMode)    ## 烟感和红外
class EventsRawModeAdmin(admin.ModelAdmin):
    list_display = ('devicetype','messagetype','mac', "smokeid", 'statedesc', 'tvalue', 'dataunit','data','devicename')
    search_fields = ('deviceID',)
    list_filter = ('smokeid', 'devicetype')