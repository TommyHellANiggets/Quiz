# Generated by Django 5.1.3 on 2024-11-09 21:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='answered_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время ответа'),
        ),
    ]
