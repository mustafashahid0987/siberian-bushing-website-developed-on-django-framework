# Generated by Django 3.2.21 on 2023-10-17 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0021_rename_discount_discount_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discount_table',
            old_name='user',
            new_name='user_ids',
        ),
    ]
