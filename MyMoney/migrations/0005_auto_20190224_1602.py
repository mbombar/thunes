# Generated by Django 2.1.4 on 2019-02-24 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyMoney', '0004_expense_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]