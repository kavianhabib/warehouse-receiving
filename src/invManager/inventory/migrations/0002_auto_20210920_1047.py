# Generated by Django 3.2.5 on 2021-09-20 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='number_ordered',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='number_received',
            field=models.IntegerField(default=0, null=True),
        ),
    ]