# Generated by Django 5.0.6 on 2024-06-15 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_alter_buystock_options_buystock_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='buystock',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
