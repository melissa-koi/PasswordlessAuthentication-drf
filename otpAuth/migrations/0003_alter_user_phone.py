# Generated by Django 3.2.7 on 2021-10-04 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otpAuth', '0002_alter_user_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=8),
        ),
    ]
