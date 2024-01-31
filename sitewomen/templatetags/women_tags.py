'''
создаем свой тег и можем им пользоваться в любом нашем шаблоне
также обязательно питоновский файл __init__.py всё это далжно находиться в папке tamplatetags
'''
from django import template
import sitewomen.views as views
from sitewomen.models import Category, TagPost2 # импорт из моделей классы таблиц
from django.db.models import Count # импорт метода Count для опубликования тегов только тех у которых есть данные

from sitewomen.utils import menu

register = template.Library() # экземпляр класса Library для регистрации новых тегов, вроде как декоратор

# @register.simple_tag(name='getcats') # декоратор который регистрирует в себе функцию (простой тег позволяет выносить на страницу данные
# def get_categories(): # возврат категорий постов
#     return views.cats_db

@register.simple_tag()  # делаем информацию в тег для пердачи на страницу base.html
def get_menu():
    return menu


@register.inclusion_tag('women/list_categories.html') # влючающий тег позволяет выводить на страницу прям целые элементы html в параметре узазываем путь что планируем вывести (шаблонный тег) в данном случае выводим на главную страницу меню с все категории - актрисы - певицы
def show_categories(cat_selected=0): # параметр для того чтобы ссылочка подсвечивалась он будет отвечать за выбранную категорию
    # cats = Category.objects.all() # страрый способ, чтобы вывести все категории
    cats = Category.objects.annotate(total=Count('posts')).filter(total__gt=0) # новый способ выбирает категории только которые связаны с постами
    return {'cats': cats, 'cat_selected': cat_selected} # вписываем параметр для передачи на страницу но на самой странице этот параметр нужно обработать через проверку

@register.inclusion_tag('women/list_tags.html') # влючающий тег позволяет выводить на страницу прям целые элементы html в параметре узазываем путь что планируем вывести (шаблонный тег)
def show_all_tags(): # параметр для того чтобы ссылочка подсвечивалась он будет отвечать за выбранную категорию
    # return {'tags': TagPost2.objects.all()} # старый способкоторый выводил абсалютно все теги вписывааем параметр для передачи на страницу но на самой странице этот параметр нужно обработать через проверку
    return {'tags': TagPost2.objects.annotate(total=Count('tags')).filter(total__gt=0)} # вы водим только теги которыесвязаны с постами







