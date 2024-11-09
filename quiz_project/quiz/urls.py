from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.auth_view, name='auth'),
    path('quiz/<slug:slug>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<slug:slug>/result/', views.quiz_result, name='quiz_result'),
    path('quiz/<slug:slug>/save_answer/', views.save_quiz_answers, name='save_quiz_answers'),

]
