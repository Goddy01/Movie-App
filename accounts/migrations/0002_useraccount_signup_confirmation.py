# Generated by Django 4.1.3 on 2022-11-26 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='signup_confirmation',
            field=models.BooleanField(default=False),
        ),
    ]
