# Generated by Django 4.0.1 on 2022-02-22 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cogi', '0002_cogi_week_cogi_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cogi',
            name='created_on',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='cogi',
            name='customer_order',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cogi',
            name='customer_order_item',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cogi',
            name='division',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cogi',
            name='error_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='cogi',
            name='error_text',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cogi',
            name='matrial',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cogi',
            name='message_number',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cogi',
            name='movement_code',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cogi',
            name='order',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cogi',
            name='otp_element',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cogi',
            name='qty_unit_entered',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cogi',
            name='stock_movement_doc',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cogi',
            name='store',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cogi',
            name='time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='cogi',
            name='time_error',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='cogi',
            name='treatment_status',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
