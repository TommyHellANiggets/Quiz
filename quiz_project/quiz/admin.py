from django.contrib import admin
from .models import Quiz, Question

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1  # Сколько пустых вопросов будет добавлено по умолчанию
    max_num = 10  # Максимум 10 вопросов

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    prepopulated_fields = {"slug": ("title",)}

from django.contrib import admin
from .models import QuizResultAdmin

class QuizResultAdminAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'score', 'max_score', 'date')

admin.site.register(QuizResultAdmin, QuizResultAdminAdmin)
