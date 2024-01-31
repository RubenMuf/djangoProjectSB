from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

'''
Этот файл нужен для того чтобы в систему пользователь мог входить помимомо стандартного джанговского метода
при помощи логина и пароля, но и если в логин вводить E-mail и также пароль
'''

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model() # помещаем в переменную текущею модель пользователя
        try:
            user = user_model.objects.get(email=username) # получаем пользователя по модели по параметру email
            if user.check_password(password): # проверяем пароль, готовый метод из джанго
                return user
            return None
        except (user_model.DoesNotExist, get_user_model().MultipleObjectsReturned): # исключения: 1й не нашли такого пользователя, 2й нашле несколько пользователей с таким email
            return None # так как прошли в except - возвращаем None

    def get_user(self, user_id): # метод чтобы система видела, что пользователь зашел, 2й параметр меткак по id текушего пользователя
        user_model = get_user_model() # получаем текущую модель
        try:
            return user_model.objects.get(pk=user_id) # получаем через фильтр текущего пользователя
        except user_model.DoesNotExist: # исключение, если нет такого пользователь
            return None


