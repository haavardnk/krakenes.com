# Generated by Django 3.0.3 on 2020-02-15 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_category_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='description',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(default='test', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='summary',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
