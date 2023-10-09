# Generated by Django 4.2.4 on 2023-09-11 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.ForeignKey(blank=True, db_column='user_type', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usertype', to='accounts.usertype'),
        ),
    ]