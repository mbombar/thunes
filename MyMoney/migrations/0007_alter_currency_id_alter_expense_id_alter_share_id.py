# Generated by Django 4.1.2 on 2022-10-13 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyMoney', '0006_auto_20190224_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='share',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
