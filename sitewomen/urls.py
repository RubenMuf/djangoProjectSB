from django.urls import path, re_path, register_converter
from . import views
from . import converters
from sitewomen.views import page_not_found

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.WomenHome.as_view(), name='home'), # представление через класс, () - обязательны так как вызываем метод из класса
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'), # представление через класс, () - обязательны так как вызываем метод из класса
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('edit/<int:pk>/', views.UpdatePage.as_view(), name='edit_page') # для редактирования статьи










    # path('cats/<int:cat_id>/', views.categories, name='cats1'),
    # path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'),
    # path('archive/<year4:year>/', views.archive, name='archive')

    # re_path(r'^archive/(?P<year>[0-9]{4}/)', views.archive)  # используем регулярные выражения
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