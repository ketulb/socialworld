# Generated by Django 4.0.5 on 2022-06-14 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_remove_profile_first_name_profile_last_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='Last_name',
            new_name='lastname',
        ),
        migrations.AddField(
            model_name='profile',
            name='firstname',
            field=models.TextField(default=2, max_length=50),
            preserve_default=False,
        ),
    ]