# Generated by Django 4.1.3 on 2022-11-26 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_useraccount_signup_confirmation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
