# Generated by Django 5.1.1 on 2024-09-26 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0003_alter_author_options_rename_first_name_author_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='author_id',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]