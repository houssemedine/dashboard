# Generated by Django 4.0.1 on 2022-08-09 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_accuracy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sq00',
            name='company',
            field=models.CharField(max_length=50, null=True),
        ),
    ]