# Generated by Django 3.2.21 on 2023-10-13 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_bank_details_zelle_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_proof',
            field=models.FileField(default='None', null=True, upload_to='media'),
        ),
    ]
