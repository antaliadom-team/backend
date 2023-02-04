# Generated by Django 3.2.16 on 2023-02-03 21:01

import api.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30, validators=[api.validators.validate_name], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=30, validators=[api.validators.validate_name], verbose_name='Фамилия'),
        ),
    ]
