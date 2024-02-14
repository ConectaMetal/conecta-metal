# Generated by Django 5.0.1 on 2024-02-14 19:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0021_alter_products_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buycart',
            name='customer',
        ),
        migrations.AddField(
            model_name='buycart',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.userprofile'),
        ),
        migrations.AlterField(
            model_name='buycart',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.products'),
        ),
    ]
