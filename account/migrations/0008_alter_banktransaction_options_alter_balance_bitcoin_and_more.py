# Generated by Django 5.0.6 on 2024-06-21 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_balance_bitcoin_alter_balance_etheriun'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banktransaction',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterField(
            model_name='balance',
            name='bitcoin',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='balance',
            name='etheriun',
            field=models.FloatField(default=0.0),
        ),
    ]
