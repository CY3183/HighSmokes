from django.db import models


class LocaltionInfo(models.Model):
    '''位置信息表'''
    device_id = models.CharField(verbose_name='设备id',max_length=64)
    location = models.CharField(verbose_name='地址',max_length=64)


class EventsRawMode(models.Model):
    '''接收烟感和红外事件'''
    ccc = models.CharField(max_length=64, null=True,blank=True, verbose_name="CCC")
    mac = models.CharField(max_length=64,null=True, blank=True, verbose_name="设备号唯一编码")
    ccid = models.CharField(max_length=64, null=True, blank=True, verbose_name="CCID")
    imei = models.CharField(max_length=64, null=True, blank=True, verbose_name="imei")
    imsi = models.CharField(max_length=64, null=True, blank=True, verbose_name="imsi")
    cstatus = models.CharField(max_length=64, null=True, blank=True, verbose_name="cstatus")
    dsignal = models.CharField(max_length=64, null=True, blank=True, verbose_name="dsignal")
    smokeid = models.CharField(max_length=64, null=True, blank=True, verbose_name="设备ID")
    batterys = models.CharField(max_length=64, null=True, blank=True, verbose_name="batterys")
    createtime = models.CharField(max_length=64, null=True, blank=True, verbose_name="精确到毫秒")
    devicetype = models.CharField(max_length=64, null=True, blank=True, verbose_name="设备类型")
    messagetype = models.CharField(max_length=64, null=True, blank=True, verbose_name="事件类型")
    businesstype = models.CharField(max_length=64, null=True, blank=True, verbose_name="businesstype")
    tamperstatus = models.CharField(max_length=64, null=True, blank=True, verbose_name="tamperstatus")
    voltagevalue = models.CharField(max_length=64, null=True, blank=True, verbose_name="通道名称")
    xdsmokelogid = models.CharField(max_length=64, null=True, blank=True, verbose_name="消息ID")
    statedesc = models.CharField(max_length=64, null=True, blank=True, verbose_name="告警内容")
    tvalue = models.CharField(max_length=64, null=True, blank=True, verbose_name="监测温度，单位°C")
    dataunit = models.CharField(max_length=64, null=True, blank=True, verbose_name="监测单位")
    data = models.CharField(max_length=64, null=True, blank=True, verbose_name="监测值")
    devicename = models.CharField(max_length=64, null=True, blank=True, verbose_name="设备位置")




