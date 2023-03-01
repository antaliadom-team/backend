# Generated by Django 3.2.16 on 2023-03-01 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('catalog', '0007_order_is_sent')]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(
                choices=[('Аренда', 'Аренда'), ('Покупка', 'Покупка')],
                db_index=True,
                default='Аренда',
                max_length=7,
                unique=True,
                verbose_name='Категория объекта',
            ),
        ),
        migrations.AlterField(
            model_name='order',
            name='rooms',
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
                verbose_name='Количество комнат',
            ),
        ),
    ]
