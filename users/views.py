from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import LoginUsersForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


# Create your views here.

class Login_user(LoginView):
    form_class = LoginUsersForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    # def get_success_url(self): # метод для перенаправления на страницу если юзер зарегистрировался, но его комментим так как есть путь- константаllllll прописанный в settings LOGIN_REDIRECT_URL = 'home'
    #     return reverse_lazy('home')

class RegistrUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')  # маршрут куда попадает пользователь после регистрации

# def register(request): # старая функция представления регистрации
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST) # создаем форму с данными которые были переданы(ставим из в параметры в скобки)
#         if form.is_valid(): # если форма заполнена праильна - проверка проверка уже внутри пайчарма
#             user = form.save(commit=False) # формируем пользователя, но пока не заносим его в БД
#             user.set_password(form.cleaned_data['password']) # шифруем пароль с помощью этого метода
#             user.save()
#             return render(request, 'users/register_done.html')
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя'}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None): # метод защита, чтобы редактировать профиль мог только пользователь-хозяин профиля
        return self.request.user

class UsersPasswordChange(PasswordChangeView): # класс изменения пароля, основан на ГР классе в джанго
    form_class = UserPasswordChangeForm # строим его на классе из формы, чтобы отобраражились стили нашего сайта, а не админ панели
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"



