# Generated by Django 3.0.2 on 2020-07-11 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bd', '0007_auto_20200711_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servers',
            name='iv',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
