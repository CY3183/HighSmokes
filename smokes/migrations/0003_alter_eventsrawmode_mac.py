# Generated by Django 4.2.11 on 2024-03-13 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smokes', '0002_eventsrawmode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventsrawmode',
            name='mac',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='设备号唯一编码'),
        ),
    ]