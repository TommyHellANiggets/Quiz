from django.db import models
from django.utils.text import slugify

from django.contrib.auth.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название квиза")
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    title = models.CharField(max_length=255, verbose_name="Заголовок вопроса")
    description = models.TextField(blank=True, verbose_name="Описание вопроса")
    image = models.ImageField(upload_to="question_images/", blank=True, null=True, verbose_name="Фото вопроса")

    # Поля для вариантов ответов
    answer_a = models.CharField(max_length=255, verbose_name="Вариант А")
    answer_b = models.CharField(max_length=255, verbose_name="Вариант Б")
    answer_c = models.CharField(max_length=255, verbose_name="Вариант В")
    answer_d = models.CharField(max_length=255, verbose_name="Вариант Г")

    # Поля для баллов за каждый вариант ответа
    score_a = models.IntegerField(default=0, verbose_name="Баллы за Вариант А")
    score_b = models.IntegerField(default=0, verbose_name="Баллы за Вариант Б")
    score_c = models.IntegerField(default=0, verbose_name="Баллы за Вариант В")
    score_d = models.IntegerField(default=0, verbose_name="Баллы за Вариант Г")

    # Поле для хранения правильного ответа
    correct_answer = models.CharField(
        max_length=1,
        choices=[('a', 'A'), ('b', 'Б'), ('c', 'В'), ('d', 'Г')],
        verbose_name="Правильный ответ"
    )

    def __str__(self):
        return f"{self.quiz.title} - {self.title}"


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], verbose_name="Выбранный ответ")
    score = models.IntegerField(default=0)
    answered_at = models.DateTimeField(default=timezone.now, verbose_name="Время ответа")

    class Meta:
        unique_together = ('user', 'quiz', 'question')


from django.db import models

class QuizResultAdmin(models.Model):
    user_id = models.IntegerField()  # ID пользователя
    username = models.CharField(max_length=100)  # Логин
    score = models.IntegerField()  # Набранный балл
    max_score = models.IntegerField()  # Максимальный балл
    date = models.DateTimeField(auto_now_add=True)  # Дата
