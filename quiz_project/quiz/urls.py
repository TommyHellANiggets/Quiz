from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.auth_view, name='auth'),
    path('profile/', views.profile_view, name='profile'),
    path('quiz/<slug:slug>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<slug:slug>/result/', views.quiz_result, name='quiz_result'),
    path('quiz/<slug:slug>/save_answer/', views.save_quiz_answers, name='save_quiz_answers'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

]
