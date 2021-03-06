# Generated by Django 3.0.3 on 2020-05-13 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0019_auto_20200513_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='image',
            field=models.ImageField(upload_to='images/albums'),
        ),
        migrations.AlterField(
            model_name='site',
            name='background',
            field=models.ImageField(upload_to='images/sites'),
        ),
    ]
