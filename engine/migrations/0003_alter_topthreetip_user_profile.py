# Generated by Django 5.0.1 on 2024-01-20 22:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0002_remove_userprofile_contact_information_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topthreetip',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tips', to='engine.userprofile'),
        ),
    ]