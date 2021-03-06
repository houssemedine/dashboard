# Generated by Django 4.0.1 on 2022-02-28 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_requisition', models.CharField(max_length=50)),
                ('item_of_requisition', models.CharField(max_length=10)),
                ('deletion_indicator', models.CharField(max_length=20)),
                ('purchasing_group', models.CharField(max_length=20)),
                ('division', models.CharField(max_length=20)),
                ('requisition_date', models.DateField()),
                ('release_date', models.DateField()),
                ('outline_agreement', models.CharField(max_length=20)),
                ('principal_agmt_item', models.CharField(max_length=20)),
                ('purchase_order', models.CharField(max_length=20)),
                ('purchase_order_item', models.CharField(max_length=20)),
            ],
        ),
    ]
