# Generated by Django 3.0.7 on 2020-07-01 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0021_remove_photo_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='photo1',
            field=models.ImageField(blank=True, upload_to='images/sites'),
        ),
        migrations.AddField(
            model_name='site',
            name='text1',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='site',
            name='text2',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
