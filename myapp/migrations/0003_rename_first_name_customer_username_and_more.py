# Generated by Django 5.1.4 on 2025-01-15 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='first_name',
            new_name='UserName',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='last_name',
        ),
    ]
