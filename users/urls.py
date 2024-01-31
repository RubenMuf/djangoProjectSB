from django.contrib.auth.views import LogoutView, AuthenticationForm, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
from .import views
from .views import Login_user

app_name = 'users'

urlpatterns = [
    path('login/', Login_user.as_view(), name='login'), # представление через класс, () - обязательны так как вызываем метод из класса
    path('logout/', LogoutView.as_view(), name='logout'), # представление через класс, () - обязательны так как вызываем метод из класса

    # path('password_change/', PasswordChangeView.as_view(), name='password_change'), # этот класс для обработки формы изменения пароля (старый медод, который открывает страницу джанго, ниже прописали путь который открывает нашу собственную сделанную страницу
    path('password_change/', views.UsersPasswordChange.as_view(), name='password_change'), # новый путь для изменеия пароля на своей форме, но которая на классе из джанго, чтобы страница была своя со своими стилями
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'), # для отображения результата успешного изменения пароля, прямо здесь указываем параметр какую страницу открывать после выполнения класса представления

    path('password-reset/',
         PasswordResetView.as_view(
             template_name='users/password_reset_form.html', # шаблон для отображения формы
             email_template_name='users/password_reset_email.html', # шаблон для формирования сообщения текста электронной почты
             success_url=reverse_lazy('users:password_reset_done') # какую страницу открыть после восстановления пароля
         ),
             name='password_reset'), # путь для восстановления пароля на стандартном классе
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name='users/password_reset_form.html'),
         name='password_reset_done'), # путь для показа подверждения отправки инструкции для восстановления пароля

    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             success_url=reverse_lazy('users:password_reset_done')),
             name='password_reset_confirm'), # путь для того чтобы пользователь ввел новый пароль
    path('password-reset/complete/', # путь ля информационного собщения что пароль изменен
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('register/', views.RegistrUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
]









'''
<int:catid>/ пример
str - любая не пустая строка исключая символ '/'
int - любое положительное число, включая 0
slug - слаг, тоесть латиница ASCII таблицы, символы дефиса и подчеркивания
uuid - цифры, малые латинские символы ASCII, дефис
path - любая не пустая строка, включая символ '/'
re_path - для использования регулярных выражений для проверки введенного запроса
'''