from django.db import models


class EventsRawMode(models.Model):
    '''接收高空抛物事件'''
    portNo = models.CharField(max_length=64, null=True,blank=True, verbose_name="端口号")
    dateTime = models.DateTimeField(null=True, blank=True, verbose_name="告警时间")
    deviceID = models.CharField(max_length=64, null=True, blank=True, verbose_name="设备ID")
    protocol = models.CharField(max_length=64, null=True, blank=True, verbose_name="protocol")
    channelID = models.CharField(max_length=64, null=True, blank=True, verbose_name="channelID")
    eventType = models.CharField(max_length=64, null=True, blank=True, verbose_name="事件类型")
    ipAddress = models.CharField(max_length=64, null=True, blank=True, verbose_name="IP")
    eventState = models.CharField(max_length=64, null=True, blank=True, verbose_name="事件状态")
    macAddress = models.CharField(max_length=64, null=True, blank=True, verbose_name="设备MAC")
    channelName = models.CharField(max_length=64, null=True, blank=True, verbose_name="通道名称")
    ipv6Address = models.CharField(max_length=64, null=True, blank=True, verbose_name="ipv6")
    protocolType = models.CharField(max_length=64, null=True, blank=True, verbose_name="protocolType")
    activePostCount = models.CharField(max_length=64, null=True, blank=True, verbose_name="activePostCount")
    eventDescription = models.CharField(max_length=64, null=True, blank=True, verbose_name="事件描述")
    isDataRetransmission = models.CharField(max_length=64, null=True, blank=True, verbose_name="isDataRetransmission")
