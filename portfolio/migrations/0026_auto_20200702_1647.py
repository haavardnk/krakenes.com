# Generated by Django 3.0.7 on 2020-07-02 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0025_auto_20200701_1657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='description',
        ),
        migrations.AlterField(
            model_name='photo',
            name='album',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='portfolio.Album'),
            preserve_default=False,
        ),
    ]
