from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.urls import reverse

User = get_user_model()

def auth_view(request):
    next_url = request.GET.get('next', 'base')  # Получаем next из GET-параметра

    if request.method == 'POST':
        if 'login-btn' in request.POST:
            email = request.POST.get('email-login')
            password = request.POST.get('password-login')

            # Аутентификация пользователя по email и паролю
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect(next_url)  # Редирект на next после успешного входа
            else:
                messages.error(request, 'Неверные данные для входа')

        elif 'register-btn' in request.POST:
            # Обработка регистрации
            name = request.POST.get('name-register')
            email = request.POST.get('email-register')
            password = request.POST.get('password-register')

            # Проверка, существует ли уже пользователь с таким email
            if not User.objects.filter(email=email).exists():
                # Создание нового пользователя
                user = User.objects.create_user(
                    username=email,  # Используем email как уникальное имя пользователя
                    email=email,
                    password=password
                )
                user.save()
                messages.success(request, 'Регистрация успешна! Пожалуйста, войдите.')

                # Редирект на страницу авторизации с сохраненным параметром next
                return redirect(f"{reverse('auth')}?next={next_url}")
            else:
                messages.error(request, 'Пользователь с таким email уже существует')

    # Передаем next в шаблон, чтобы сохранить его при регистрации
    return render(request, 'auth.html', {'next': next_url})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz

@login_required  # Используем декоратор, чтобы гарантировать, что пользователь авторизован
def quiz_detail(request, slug):
    quiz = get_object_or_404(Quiz, slug=slug)
    questions_with_choices = []

    for question in quiz.questions.all():
        choices = [
            ('a', question.answer_a),
            ('b', question.answer_b),
            ('c', question.answer_c),
            ('d', question.answer_d)
        ]
        questions_with_choices.append({
            'question': question,
            'choices': choices
        })

    context = {
        'quiz': quiz,
        'questions_with_choices': questions_with_choices,
        'quiz_id': quiz.id  # Передаем quiz.id
    }
    return render(request, 'index.html', context)


import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Quiz, UserAnswer, Question

@csrf_exempt  # Уберите это, если хотите использовать CSRF-токен
def save_quiz_answers(request, slug):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, slug=slug)

        # Проверка и получение данных
        try:
            data = json.loads(request.body)
            answers = data.get('answers', {})
            print(f"Received answers: {answers}")
        except json.JSONDecodeError:
            print("Invalid JSON data received")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        # Обработка каждого ответа
        for question_index, answer_value in answers.items():
            try:
                question = quiz.questions.get(id=int(question_index))

                # Получение баллов для выбранного ответа
                score = 0
                if answer_value == 'a':
                    score = question.score_a
                elif answer_value == 'b':
                    score = question.score_b
                elif answer_value == 'c':
                    score = question.score_c
                elif answer_value == 'd':
                    score = question.score_d

                # Сохранение ответа и баллов
                UserAnswer.objects.update_or_create(
                    user=request.user if request.user.is_authenticated else None,
                    quiz=quiz,
                    question=question,
                    defaults={'selected_answer': answer_value, 'score': score}
                )
                print(f"Saved answer for question ID {question_index}: {answer_value} with score {score}")

            except Question.DoesNotExist:
                print(f"Question with ID {question_index} not found.")
                return JsonResponse({'error': f'Question with ID {question_index} not found.'}, status=404)
            except ValueError:
                print(f"Invalid question ID format: {question_index}")
                return JsonResponse({'error': f'Invalid question ID: {question_index}'}, status=400)

        return JsonResponse({'status': 'success'})

    print("Invalid request method")
    return JsonResponse({'error': 'Invalid request method'}, status=405)



@login_required
def quiz_result(request, slug):
    # Получаем квиз по slug
    quiz = get_object_or_404(Quiz, slug=slug)

    # Получаем все вопросы квиза
    questions = quiz.questions.all()

    # Считаем максимальное количество баллов за квиз (используем max для каждого вопроса)
    total_score = sum(
        max(question.score_a, question.score_b, question.score_c, question.score_d)
        for question in questions
    )

    # Получаем ответы пользователя на вопросы
    user_answers = UserAnswer.objects.filter(user=request.user, quiz=quiz)

    # Считаем фактическое количество баллов, набранных пользователем
    user_score = sum(user_answer.score for user_answer in user_answers)

    # Список для хранения результатов по каждому вопросу
    question_results = []

    # Создаем два списка для графика
    question_labels = []
    correct_percentages = []

    for idx, question in enumerate(questions, 1):  # Начнем нумерацию с 1
        # Получаем ответ пользователя на текущий вопрос
        user_answer = user_answers.filter(question=question).first()
        # Если пользователь ответил, то берем его баллы, если нет, то 0
        user_answer_score = user_answer.score if user_answer else 0
        # Максимальный балл за вопрос
        max_question_score = max(question.score_a, question.score_b, question.score_c, question.score_d)

        # Подсчитываем процент правильных ответов на вопрос
        correct_count = UserAnswer.objects.filter(
            question=question,
            selected_answer=question.correct_answer
        ).count()
        total_count = UserAnswer.objects.filter(question=question).count()
        correct_percentage = (correct_count / total_count) * 100 if total_count > 0 else 0

        # Добавляем в список результаты
        question_results.append({
            'question_number': idx,
            'user_answer_score': user_answer_score,
            'max_question_score': max_question_score,
            'correct_answer': question.correct_answer,
            'user_answer': user_answer.selected_answer if user_answer else None,
            'correct_percentage': correct_percentage,
        })

        # Добавляем данные для графика
        question_labels.append(f'Вопрос {idx}')
        correct_percentages.append(correct_percentage)

    # В views.py
    context = {
        'quiz': quiz,
        'total_score': total_score,
        'user_score': user_score,
        'question_results': question_results,
        'question_labels': question_labels,
        'correct_percentages': correct_percentages,
    }

    return render(request, 'result.html', context)



from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib import messages
from .models import Quiz, UserAnswer


@login_required
def profile_view(request):
    # Handle password change
    if request.method == 'POST':
        if 'change_password' in request.POST:
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')

            if request.user.check_password(old_password):
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Keep user logged in after password change
                messages.success(request, 'Password changed successfully.')
            else:
                messages.error(request, 'Old password is incorrect.')

        elif 'logout' in request.POST:
            logout(request)
            return redirect('auth')  # Redirect to login page after logout

    # Get quiz results for the user
    user_quiz_results = []
    quizzes_taken = UserAnswer.objects.filter(user=request.user).values('quiz').distinct()

    for quiz_data in quizzes_taken:
        quiz = Quiz.objects.get(id=quiz_data['quiz'])

        # Calculate the total score for the quiz
        total_score = sum(
            question.score_a + question.score_b + question.score_c + question.score_d
            for question in quiz.questions.all()
        )

        # Calculate the user's score for the quiz
        user_score = UserAnswer.objects.filter(user=request.user, quiz=quiz).aggregate(user_score=Sum('score'))[
            'user_score']

        # Append quiz result to the list
        user_quiz_results.append({
            'quiz_title': quiz.title,
            'user_score': user_score,
            'total_score': total_score
        })

    context = {
        'user_id': request.user.id,
        'user_username': request.user.username,
        'user_email': request.user.email,
        'quiz_results': user_quiz_results,
    }

    return render(request, 'profile.html', context)


from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'  # Укажите свой шаблон, если нужен
    success_url = reverse_lazy('password_change_done')

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'  # Укажите свой шаблон, если нужен


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import UserAnswer, Question, QuizResultAdmin


@receiver(post_save, sender=UserAnswer)
def save_quiz_result(sender, instance, **kwargs):
    # Получаем данные для пользователя и квиза
    user_id = instance.user.id
    quiz_id = instance.quiz.id

    # Вычисляем общее количество баллов пользователя за квиз
    total_score = UserAnswer.objects.filter(user_id=user_id, quiz_id=quiz_id).aggregate(total=Sum('score'))['total']

    # Вычисляем максимальный возможный балл за квиз
    max_score = Question.objects.filter(quiz_id=quiz_id).aggregate(
        max_total=Sum('score_a') + Sum('score_b') + Sum('score_c') + Sum('score_d')
    )['max_total']

    # Получаем имя пользователя и дату
    username = instance.user.username
    date = instance.answered_at

    # Создаем новую запись в таблице QuizResultAdmin
    QuizResultAdmin.objects.create(
        user_id=user_id,
        username=username,
        score=total_score,
        max_score=max_score,
        date=date,
    )
