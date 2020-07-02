# Generated by Django 3.0.7 on 2020-07-02 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0026_auto_20200702_1647'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['order'], 'verbose_name_plural': 'Photos'},
        ),
        migrations.AddField(
            model_name='photo',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
