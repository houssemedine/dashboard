# Generated by Django 4.0.1 on 2022-03-03 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchasepast', '0003_alter_purchase_deletion_indicator_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='transferring_division',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='valuation_price',
            field=models.FloatField(null=True),
        ),
    ]
