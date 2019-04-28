# Generated by Django 2.2 on 2019-04-23 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190423_2129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='age',
            new_name='level',
        ),
        migrations.AlterField(
            model_name='attribute',
            name='start_max',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='start_min',
            field=models.IntegerField(default=80),
        ),
    ]
