# Generated by Django 4.2.5 on 2023-11-16 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitewomen', '0002_alter_women_options_women_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='women',
            name='slug',
            field=models.SlugField(max_length=225, unique=True),
        ),
    ]
