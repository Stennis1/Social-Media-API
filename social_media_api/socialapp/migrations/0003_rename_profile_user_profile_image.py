# Generated by Django 5.2 on 2025-04-03 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0002_alter_post_image_alter_user_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='profile',
            new_name='profile_image',
        ),
    ]
