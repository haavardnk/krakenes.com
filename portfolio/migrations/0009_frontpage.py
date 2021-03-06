# Generated by Django 3.0.3 on 2020-05-08 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_auto_20200425_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frontpage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('sub_title', models.CharField(blank=True, max_length=75)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.Photo')),
            ],
        ),
    ]
