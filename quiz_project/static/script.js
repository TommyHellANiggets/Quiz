document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const loginBtn = document.getElementById('login-btn');
    const registerBtn = document.getElementById('register-btn');

    // Функция для переключения формы
    function showLoginForm() {
        loginForm.style.display = 'flex';
        registerForm.style.display = 'none';

        // Меняем цвет текста кнопок
        loginBtn.style.color = '#0066FF'; // Синий цвет для активной кнопки
        registerBtn.style.color = '#838AA7'; // Белый цвет для неактивной кнопки
    }

    function showRegisterForm() {
        registerForm.style.display = 'flex';
        loginForm.style.display = 'none';

        // Меняем цвет текста кнопок
        registerBtn.style.color = '#0066FF'; // Синий цвет для активной кнопки
        loginBtn.style.color = '#838AA7'; // Белый цвет для неактивной кнопки
    }

    // Обработчики событий для кнопок
    loginBtn.addEventListener('click', showLoginForm);
    registerBtn.addEventListener('click', showRegisterForm);

    // Изначально показываем форму авторизации
    showLoginForm();
});


document.addEventListener('DOMContentLoaded', function () {
  const togglePasswordBtns = document.querySelectorAll('.toggle-password-btn');
  
  togglePasswordBtns.forEach(btn => {
    btn.addEventListener('click', function () {
      const passwordInput = btn.previousElementSibling;
      const showIcon = btn.querySelector('.show-icon');
      const hideIcon = btn.querySelector('.hide-icon');

      // Переключаем тип поля ввода пароля
      if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        showIcon.style.display = 'none';
        hideIcon.style.display = 'block';
      } else {
        passwordInput.type = 'password';
        showIcon.style.display = 'block';
        hideIcon.style.display = 'none';
      }
    });
  });
});
