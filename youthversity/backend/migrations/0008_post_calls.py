# Generated by Django 3.0.4 on 2020-03-22 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20200322_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='calls',
            field=models.PositiveIntegerField(default=0),
        ),
    ]