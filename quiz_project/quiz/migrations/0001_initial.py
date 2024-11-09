# Generated by Django 5.1.3 on 2024-11-09 19:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название квиза')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок вопроса')),
                ('description', models.TextField(blank=True, verbose_name='Описание вопроса')),
                ('image', models.ImageField(blank=True, null=True, upload_to='question_images/', verbose_name='Фото вопроса')),
                ('answer_a', models.CharField(max_length=255, verbose_name='Вариант А')),
                ('answer_b', models.CharField(max_length=255, verbose_name='Вариант Б')),
                ('answer_c', models.CharField(max_length=255, verbose_name='Вариант В')),
                ('answer_d', models.CharField(max_length=255, verbose_name='Вариант Г')),
                ('score_a', models.IntegerField(default=0, verbose_name='Баллы за Вариант А')),
                ('score_b', models.IntegerField(default=0, verbose_name='Баллы за Вариант Б')),
                ('score_c', models.IntegerField(default=0, verbose_name='Баллы за Вариант В')),
                ('score_d', models.IntegerField(default=0, verbose_name='Баллы за Вариант Г')),
                ('correct_answer', models.CharField(choices=[('a', 'A'), ('b', 'Б'), ('c', 'В'), ('d', 'Г')], max_length=1, verbose_name='Правильный ответ')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected_answer', models.CharField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], max_length=1, verbose_name='Выбранный ответ')),
                ('score', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'quiz', 'question')},
            },
        ),
    ]