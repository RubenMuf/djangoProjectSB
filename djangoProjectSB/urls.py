"""
Настройка URL-адреса для проекта django ProjectS B.

Список "urlpatterns" перенаправляет URL-адреса в представления. Для получения дополнительной информации, пожалуйста, смотрите:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Примеры:
Функциональные представления
    1. Добавьте импорт: из представлений импорта my_app
    2. Добавьте URL в urlpatterns: path(", views.home, name='главная')
Представления на основе классов
    1. Добавьте импорт: из other_app.views импортируйте Home
    2. Добавьте URL в urlpatterns: path(", Home.as_view(), name='home')
Включая другой URLconf
    1. Импортируйте функцию include(): из django.urls импортируйте include, путь
    2. Добавьте URL в urlpatterns: path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from djangoProjectSB import settings
from sitewomen.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sitewomen.urls')), # перенаправка на другой urls
    path('users/', include('users.urls', namespace='users')), # перенаправка на другой urls связанный с авторизацией на сайте, 2-й параметр обязателен для полей имен
    path("__debug__/", include("debug_toolbar.urls")), # для джангодебага

]

if settings.DEBUG: # чтобы в режиме отладки к маршруту добавлялась префикс медиа
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# обработчик если страница не опреледена
handler404 = page_not_found

admin.site.site_header = 'Панель администрирования'  # замена в кабинете админа заголовка
admin.site.index_title = 'Известные женщины мира'  # замена в кабинете админа заголовка