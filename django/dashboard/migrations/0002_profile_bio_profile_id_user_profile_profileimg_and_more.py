# Generated by Django 4.0.5 on 2022-06-13 23:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='id_user',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='profile',
            name='profileimg',
            field=models.ImageField(default='blank-profile-picture.png', upload_to='profile_images'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]