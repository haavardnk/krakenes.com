# Generated by Django 2.2.8 on 2020-01-22 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20190508_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='description',
            field=models.TextField(blank=True, max_length=30),
        ),
    ]