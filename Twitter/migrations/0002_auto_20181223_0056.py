# Generated by Django 2.0.5 on 2018-12-22 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Twitter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(default=None, null=True),
        ),
    ]