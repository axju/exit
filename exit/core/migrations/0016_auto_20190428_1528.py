# Generated by Django 2.2 on 2019-04-28 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20190427_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='description',
            field=models.TextField(default='...', verbose_name='description'),
        ),
    ]