from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages

User = get_user_model()

def auth_view(request):
    # Если запрос POST, то обрабатываем форму
    if request.method == 'POST':
        if 'login-btn' in request.POST:
            email = request.POST.get('email-login')
            password = request.POST.get('password-login')

            # Аутентификация пользователя по email и паролю
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)

                # Получаем параметр next, если он есть, иначе редиректим на 'base'
                next_url = request.GET.get('next', 'base')
                return redirect(next_url)
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
                return redirect('auth')  # Редирект на страницу авторизации
            else:
                messages.error(request, 'Пользователь с таким email уже существует')

    return render(request, 'auth.html')


from django.shortcuts import render, get_object_or_404
from .models import Quiz

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


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Quiz, UserAnswer, Question


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
                UserAnswer.objects.update_or_create(
                    user=request.user if request.user.is_authenticated else None,
                    quiz=quiz,
                    question=question,
                    defaults={'selected_answer': answer_value}
                )
                print(f"Saved answer for question ID {question_index}: {answer_value}")
            except Question.DoesNotExist:
                print(f"Question with ID {question_index} not found.")
                return JsonResponse({'error': f'Question with ID {question_index} not found.'}, status=404)
            except ValueError:
                print(f"Invalid question ID format: {question_index}")
                return JsonResponse({'error': f'Invalid question ID: {question_index}'}, status=400)

        return JsonResponse({'status': 'success'})

    print("Invalid request method")
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def quiz_result(request, slug):
    quiz = get_object_or_404(Quiz, slug=slug)
    user_answers = UserAnswer.objects.filter(user=request.user, quiz=quiz)

    if not user_answers:
        return render(request, 'result.html', {'error': 'No answers found for this quiz.'})

    # Get the first score (or default to 0 if no score is found)
    total_score = user_answers.values_list('score', flat=True).first() or 0  # Correct field name 'score'

    # Optionally, sum the scores for all answers if you need the total score
    total_score = sum(user_answers.values_list('score', flat=True))

    return render(request, 'result.html', {'total_score': total_score, 'quiz': quiz})
