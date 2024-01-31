from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from sitewomen.forms import AddPostForm, UploadFileForm

from .models import Women, \
    Category, \
    TagPost2, \
    UploadFiles  # sitewomen можно не указавать так как мы и так находимся в этом пакете, можно оставить только точку перед models
from .utils import DataMixin

# menu = [{'title': 'О сайте', 'url_name': 'about'},
#         {'title': 'Добавить статью', 'url_name': 'add_page'},
#         {'title': 'Обратная связь', 'url_name': 'contact'},
#         {'title': 'Войти', 'url_name': 'login'}
# ]

# Create your views here/
# def index(request): # HttpRequest старый способ представления на функции, перешли на представлении на классах что более оптимально, класс ниже строкой
#     # posts = Women.objects.filter(is_published=1) # формируем из таблицы список у значений которые равны 1 то есть опубликованы. это старая запись на менеджере по умолчанию objects
#     posts = Women.publiched.all().select_related('cat') # на основе нового менеджера который мы сделали сами, select_related('cat') - чтобы не было дублирования на странице
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=data) # context=data именованный параметр'''

class WomenHome(DataMixin, ListView): # ListView автоматическое формирование таблицы с данными, но таблицу нужно указать из какой модели она составляется. Этот класс предназначен для отображения произвольных списков
    template_name = 'women/index.html' # имя шаблона в который представляем, так же как на шаблоне TemplateView или создавать страницу html - но именно с названием < имя приложения > / < имя модели > _list.html
    context_object_name = 'posts' # переменная для передачи данных на страницу список статей
    title_page = 'Главная страница'
    cat_selected = 0
    def get_queryset(self): # формирует параметр для пути, открывать выбранную позицию
        return Women.publiched.all().select_related('cat')


    # template_name = 'women/index.html' # имя шаблона в который представляем, но только на шаблоне TemplateView
    # extra_context = {                  # данные которые выгружаем на шаблон
    #     'title': 'Главная страница',
    #     'menu': menu,
    #     'posts': Women.publiched.all().select_related('cat'),
    #     'cat_selected': 0,
    # }

    # def get_context_data(self, **kwargs): # функция если есть запрос по id работает типа как параметр в функции представления (динамический параметр)
    #     contex = super().get_context_data(**kwargs)
    #     contex['title'] = 'Главная страница'
    #     contex['menu'] = menu
    #     contex['post'] = Women.publiched.all().select_related('cat')
    #     contex['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return contex

# def handle_uploaded_file(f): # готовая функция из джанго для загрузки файла-картинки в пайчарм
#     with open(f'sitewomen/uploads/{f.name}', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
@login_required # декоратор для ограничений функции в зависимости зарегистрирован ли пользователь в системе, основной путь по умолчанию прописан в settings в LOGIN_URL = 'users:login', но можно здесь индивидуально прописать в параметрах пример: LOGIN_URL = (login_url='/admin/')
def about(request): # функция для загрузки картинки от пользователя в пайчарм
    contact_list = Women.publiched.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # if request.method == 'POST':
    #     form = UploadFileForm(request.POST, request.FILES) # в параметрах передаем колекцию пост и коллекцию файлов из request
    #     if form.is_valid():
    #         # handle_uploaded_file(form.cleaned_data['file']) # SS вызываем джанговскую функцию и передаем в нее файл для загрузки картинки
    #         fp = UploadFiles(file=form.cleaned_data['file']) # создаем переменную с формой и в нее параметр который поучаем от пользователя
    #         fp.save()
    # else:
    #     form = UploadFileForm()
    return render(request, 'women/about.html', {'title': 'О сайте', 'page_obj': page_obj})

# def show_post(request, post_slug): # страрый способ представления на функции, теперь сделали на классе ниже строчка
#     post = get_object_or_404(Women, slug=post_slug) # метод из библиотеки get_object_or_404 который нужно импортировать, вытаскивает из таблицы по pk если не находит генерирует страница не найдена
#
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#     return render(request, 'women/post.html', data)

class ShowPost(DataMixin, DetailView): # класс представления детали объекта
    # model = Women #
    template_name = 'women/post.html' # страница на которой будет представление
    slug_url_kwarg = 'post_slug' # параметр который в путь для поиска именно определенного объекта в данном случае по слагу
    context_object_name = 'post' # имя объекта который представляется на странице в котором собрана необходимая информация

    def get_context_data(self, **kwargs): # навигация меню
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title) # возвращаем из метода DataMixin который написан в питонфайле utils

    def get_object(self, queryset=None): # метод для определения и представления именно опубликованной статьи
        return get_object_or_404(Women.publiched, slug=self.kwargs[self.slug_url_kwarg]) # именно здесь определяем модель по чем будут отображены статьи, в данном случает по полю опубликова

class AddPage(LoginRequiredMixin, DataMixin, CreateView):  # LoginRequiredMixin - класс для закрытия от неавторизованных пользователей, отправляет на страницу со входом в систему, а после переводит на страницу на которую пользователь хотел попасть. DataMixin - для передачи дополнительной информации.
    # form_class = AddPostForm # создаем форму, но не вызываем, а прописываем только ссылку на класс без ()
    model = Women # строим модельн на модели,
    fields = '__all__' # переносим все поля запроса от юзера, или можно списком только необходимые
    template_name = 'women/addpage.html'
    title_page = 'Добавление статьи'
    # login_url = '/admin/' # путь для перевода на определенную страницу неавторизованного пользователя

class UpdatePage(DataMixin, UpdateView): # класс для редактирование данных статьи
    model = Women  # строим модельн на модели,
    fields = ['title', 'content', 'photo', 'is_published', 'cat']  # переносим все поля запроса от юзера, или можно списком только необходимые
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home') # это формирует путь после того как форма у пользователя будет успешно и правильно заполнена и только в момент когда это путь действительно нужен
    title_page = 'Редактирование статьи' # возвращается из метода в дочернем классе DataMixin

    # def form_valid(self, form): # метод на проверку валидности формы которую заполнил юзер, в данном классе этот метод не нужен - так как он есть в этом классе в джанго
    #     form.save() # сохранение данных в таблицу
    #     return super().form_valid(form)

# class AddPage(FormView):  # на FormView
#     form_class = AddPostForm # создаем форму, но не вызываем, а прописываем только ссылку на класс без ()
#     template_name = 'women/addpage.html'
#     success_url = reverse_lazy('home')# это формирует путь после того как форма у пользователя будет успешно и правильно заполнена и только в момент когда это путь действительно нужен
#
#     extra_context = {  # данные, которые выгружаем на шаблон, в данном случае только статические - которые нам известны
#         'menu': menu,
#         'title': 'Добавление статьи',
#     }
#
#     def form_valid(self, form): # метод на проверку валидности формы которую заполнил юзер
#         form.save() # сохранение данных в таблицу
#         return super().form_valid(form)

# class AddPage(View): # на View
#     def get(self, request):
#         form = AddPostForm
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#         }
#         return render(request, 'women/addpage.html', data)
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():  # вторая проверка уже на сервере
#             form.save()  # сохранение всех данных которые пользователь заполнил на странице в табличку, это потому что мы в форме создали класс мета, который саам вытаскивает из модели поля для вывода их на траницу
#             return redirect('home')
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#         }
#         return render(request, 'women/addpage.html', data)

'''def addpage(request): # старая функция на функции представления
    if request.method == 'POST': # первая проверка на экране
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid(): # вторая проверка уже на сервере
            form.save() # сохранение всех данных которые пользователь заполнил на странице в табличку, это потому что мы в форме создали класс мета, который саам вытаскивает из модели поля для вывода их на траницу
            return redirect('home')
    else:
        form = AddPostForm()
    data = {
        'menu': menu,
        'title': 'Добавление статьи',
        'form': form
    }
    return render(request, 'women/addpage.html', data)'''
def contact(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug) # метод из библиотеки get_object_or_404 который нужно импортировать, вытаскивает из таблицы по pk если не находит генерирует страница не найдена
#     posts = Women.publiched.filter(cat_id=category.pk).select_related('cat') # select_related для чтобы не было дублей на странице
#     data = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#     return render(request, 'women/index.html', context=data)  # context=data именованный параметр

class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False # защитка - если список пуст то выскочит страница 404

    def get_queryset(self): # формирует параметр для пути, открывать выбранную позицию
        return Women.publiched.filter(cat__slug=self.kwargs['cat_slug']).select_related()

    def get_context_data(self, **kwargs): # навигация меню
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat # берем из первой записи для отображения
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk) # формируем параметры для представления на страницу
def page_not_found(request, exception): # второй параметр обязателен
    return HttpResponseNotFound('<h1>Страница не найдена!</h1>')

# def show_tag_post_list(request, tag_slug): # функция представления для отображения статей по определенному тегу мы ее убрали так как построили представление на классах что более оптимально
#     tag = get_object_or_404(TagPost2, slug=tag_slug) # метод из библиотеки get_object_or_404 который нужно импортировать, вытаскивает из таблицы по pk если не находит генерирует страница не найдена
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat') # select_related для чтобы не было дублей на странице # берем через менеджер tags который у нас указан в основной модели (tags2 = models.ManyToManyField('TagPost2', blank=True, related_name='tags'))
#
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#     return render(request, 'women/index.html', context=data)

# class TagPostList(ListView): # TagPostlist
#     template_name = 'women/index.html'
#     context_object_name = 'posts'
#     print(4)
#     allow_empty = False # защитка - если список пуст то выскочит страница 404
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         tag = TagPost2.objects.get(slug=self.kwargs['tag_slug']) # берем из первой записи для отображения
#         context['title'] = 'Тег - ' + tag.tag
#         context['menu'] = menu
#         context['cat_selected'] = None
#         return context
#
#     def get_queryset(self): # формирует параметр для пути, открывать выбранную позицию
#         return Women.publiched.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

class TagPostList(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost2.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)


    def get_queryset(self):
        return Women.publiched.filter(tags2__slug=self.kwargs['tag_slug']).select_related('cat')










































