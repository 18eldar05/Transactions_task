# Generated by Django 4.2.1 on 2024-02-28 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_accountinfo_account_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountinfo',
            name='account_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='account.account'),
        ),
    ]
