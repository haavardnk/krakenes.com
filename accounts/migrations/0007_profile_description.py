# Generated by Django 2.2.8 on 2020-01-21 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200121_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='description',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]