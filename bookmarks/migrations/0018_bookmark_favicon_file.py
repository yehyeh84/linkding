# Generated by Django 4.1 on 2023-01-07 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0017_userprofile_enable_sharing'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='favicon_file',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]
