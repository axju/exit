# Generated by Django 2.2 on 2019-04-27 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20190425_0257'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerGetAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=1)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get', to='core.Answer')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerRequireAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('min', 'Min'), ('max', 'Max')], max_length=3, verbose_name='value kind')),
                ('value', models.IntegerField(default=1)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='require', to='core.Answer')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Attribute')),
            ],
        ),
        migrations.DeleteModel(
            name='AnswerAttribute',
        ),
    ]
