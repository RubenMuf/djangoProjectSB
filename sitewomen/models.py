from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

# def translit_to_eng(s: str) -> str:  # ретранслятор для слага переводит из русских букв на английские, убрали так как есть специальная для этого автоматическая джанговская функция
#     d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
#          'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
#          'л': 'l', 'м': 'm', 'о': 'o', 'н': 'n', 'п': 'p', 'р': 'r',
#          'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
#          'ш': 'sh', 'щ': 'csch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}
#     return ''.join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))

# Create your models here.
class PublishedManager(models.Manager): # класс который наследует от стандартного класса менеджера в самом джанго для создания на основе его своего собственного менеджера для формирования списка только опубликованных статей с полем равному 1
    def get_queryset(self):
        return super().get_queryset().filter(is_published=1) # метод возвращает из базового класса, вызываем у него метод queryset и через фильтр берем только опубликованные материалы

class Women(models.Model): # чтобы было более понятно на этом классе составляется главная таблица про женщин
    class Status(models.IntegerChoices): # класс чтобы было более информативно про статус пудликации на основе IntergerChoices
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Заголовок') # 2й пар для название которое будет в админе, также годиться для формы
    slug = models.SlugField(max_length=225, unique=True, db_index=True, verbose_name='Slug') # слаг для пути 1пар - макс. длина, 2пар - уникальность, 3пар - поле индексируемое, 4пар - чтобы создавалось поле с пустым значением
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None,
                              blank=True, null=True, verbose_name='Фото')
    content = models.TextField(blank=True, verbose_name='Текст статьи') # параметр позволяет ничего не помещать в таблицу
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания') # параметр автоматически заполняет поле но только в момент добавление записи, тоесь показывает время появление записи
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения') # параметр фиксирования изменения записи
    is_published = models.BooleanField(choices=tuple(map(lambda x:(bool(x[0]), x[1]), Status.choices)), default=Status.PUBLISHED, verbose_name='Статус') # параметр по умолчанию правда статья будет опубликована, choices=tuple(map(lambda x:(bool(x[0]), x[1]) - чтобы было видно значение в админе так как нет в джанго булевого значения, у нас сейчас смотри 12-13 строчку
    # связи с другими таблицами
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категории') # многие к одному связываем наш класс с классом 'Category' через многие к одному и обязательно пишем как строка в ковычках, так как этот класс находится ниже нашего основного класса и пайчарм его попросту не увидет, вторым параметром ставим, который будет запрещать удалять категории которые не связаны с постами
    tags2 = models.ManyToManyField('TagPost2', blank=True, related_name='tags', verbose_name='Теги') # связываем с таблицей TagPost через связь многие ко многим, blank=True - потому что не каждать запись женщин будет содержать теги, related_name='tags' - чтобы мы могли через теги получать список статей которые с ними связаны. on_delete - в этой связи отсутствует. Именно через этод тэг всязываются записи с остальными. пример: a.tags2.set([tag_br, tag_o, tag_v])
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='wuman', verbose_name='Супруг') # связывам со таблицей Husband тип связи один к одному, on_delete=models.SET_NULL для того чтобы если удалить мужчину в поле оставалось Null, null=True - это допустимое значение, blank=True - также поле может быть пустым, related_name='wuman' - чтобы знать какому мужчине соответствует женщина

    objects = models.Manager() # (менеджер по умолчанию)о это для того чтобы джанговский менеджер не исчез так как мы ниже строчкой создали свой собственный
    publiched = PublishedManager() # в классе свой собственный менеджер который обрабатывает только опубликованные материалы

    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None) # get_user_model() - стандартная функция для получения модели пользователя(джанго), on_delete=models.SET_NULL - если удалить автора, то в поле статьи будет NULL, related_name='posts' - обратное связывание часто для ORM-команд, null=True - допустимое значение, default=None

    def __str__(self): # чудный метод который возврашает значение из поле title из таблицы
        return self.title

    class Meta: # класс для сортировки отображение на странице в данном случае по времени созданию записи (задать реверс поставить минус перед параметром)
        verbose_name = 'Известные женщины' # это для кабинета админа
        verbose_name_plural = 'Известные женщины' # для того чтобы этот заголовок был без в конце 's' и был в множественном числе
        ordering = ['time_create'] # сортируем по артрибуту по убыванию по умолчанию
        indexes = [
            models.Index(fields=['time_create'])
        ]

    def get_absolute_url(self): # очень важная функция, формирует адрес, также блогадаря этому методу у нас есть функция в амине посмотреть на сайте страницу конкретной женщины
        return reverse('post', kwargs={'post_slug':self.slug}) # формируем slug (берется из поля таблицы) который потом передаем в ссылку во hrev на страницу и по этой ссылке ужже создается путь в url

    # def save(self, *args, **kwargs): # для автоматического создания в кабинете администратора слуга на основе имени объекта
    #     self.slug = slugify(translit_to_eng(self.title)) # убрали этот костыль так как сделали на функции из джанго
    #     super().save(*args, **kwargs)
class Category(models.Model): # класс для связи многие к одному, чтобы было понятно на этом классе составляется таблица которая связывается с основной про женщин
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория') # имя
    slug = models.SlugField(max_length=225, unique=True, db_index=True) # для формирования пути

    class Meta: # класс для сортировки отображение на странице в данном случае по времени созданию записи (задать реверс поставить минус перед параметром)
        verbose_name = 'Категорию' # это для кабинета админа чтобы заголовок имел такое название
        verbose_name_plural = 'Категории' # для того чтобы этот заголовок был без в конце 's' и был в множественном числе
        # ordering = ['time_create'] # сортируем по артрибуту по убыванию по умолчанию
        # indexes = [
        #     models.Index(fields=['time_create'])
        # ]

    '''Здесь после миграции создается 1 новая таблица и в основной
     таблице появляется новая колонка в которой указывается id-номер
      значения из новой таблицы'''

    def __str__(self): # чудная функция для возврата одного внятного значения из поля, чтобы было понятно с чем идет работа
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug}) # формируем slug (берется из поля таблицы) который потом передаем в ссылку во hrev на страницу и по этой ссылке ужже создается путь в url

# class TagPost(models.Model): # модель для связи многие ко многим, чтобы было более понятно - на этом классе составляется талица которая связывается с основной таблицей про женщин
#     tag = models.CharField(max_length=100, db_index=True)
#     slug = models.SlugField(max_length=255, unique=True, db_index=True) #  в параметрах макс длина и чтобы было уникальным
#
#     def __str__(self):
#         return self.tag # чудный метод для возвращения, чтобы было понятно с чем работаем

class TagPost2(models.Model): # модель для связи многие ко многим, чтобы было более понятно - на этом классе составляется талица которая связывается с основной таблицей про женщин
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True) #  в параметрах макс длина и чтобы было уникальным

    '''При этом после миграции создается 2 таблицы, одна именно со значениями
    в ячейках (какие угодно, и вторая промежуточная - которая связывает основную таблицу
    с дополнительной'''

    def __str__(self):
        return self.tag # чудный метод для возвращения, чтобы было понятно с чем работаем

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug}) # формируем slug (берется из поля таблицы) который потом передаем в ссылку во hrev на страницу и по этой ссылке ужже создается путь в url

class Husband(models.Model):  # табличка для связи один к одному (мужья женщин)
    name = models.CharField(max_length=100) # поле
    age = models.IntegerField(null=True) # поле
    m_count = models.IntegerField(blank=True, default=0) # параметр - не обязательный, и по умолчанию равен 0
    def __str__(self):
        return self.name # чудный метод возврата для понятия с чем мы работаем

class UploadFiles(models.Model): # таблица для загрузки фотографий
    file = models.FileField(upload_to='uploads_model') # параметр для указания пути в какую папку загружать











