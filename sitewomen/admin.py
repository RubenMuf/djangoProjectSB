from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Women, Category  # импорт нашей модели

@admin.register(Women) # регистрация нашей модели, через декоратор
class WomenAdmin(admin.ModelAdmin): # класс чтобы в админе отображались параметры женщин
    fields = ['title', 'content', 'photo', 'post_photo', 'slug', 'cat', 'husband', 'tags2'] # отображение полей формы редактирование записей объектов
    # exclude = ['tags', 'is_published'] # альтернатива fields только он исключает что не нужно выводить, остальное выводит
    readonly_fields = ['post_photo'] # чтобы фотография выводилась в панеле редактирования
    filter_horizontal = ['tags2'] # для горизонтального и более информативного вывода тэгов
    prepopulated_fields = {'slug': ('title', )}
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat') # отображение параметров из таблицы
    list_display_links = ('title', ) # чтобы при нажатиии мышкой отрывалось по названию, а не по id
    ordering = ['time_create', 'title'] # сортировка в админе - только для админа, старая сортировка в таблице также по методу в классе Meta в модели
    list_editable = ('is_published',) # отображение значения  и возможности его редактирования в админе, но нужно поправлять в моделе параметр 'is_published', делать костыль так как нет булевого значения
    list_per_page = 5 # отображение количества статей
    actions = ['set_published', 'set_draft'] # чтобы в действиях добавилось свое собственное действие для опубликования статьи, работа в связке со строкой 18
    save_on_top = True # отображение в редакторе сохранить снизу и на сверху, по умолчанию если нет этой записи только внизу

    @admin.display(description='Фотография', ordering='content') # декоратор для названия этого метода, 2й пар для сортировки, можно указывать только который есть в таблице
    def post_photo(self, women: Women): # метод для вывода в админ для контента данной женщины
        if women.photo:
            return mark_safe(f'<img src="{women.photo.url}" width=50>') #  вывод фотографии
        else:
            return 'Без фото'
    @admin.action(description='Опубликовать статью') # декоратор для названия метода
    def set_published(self, request, queryset): # метод для того чтобы в действиях появилось собственное действие, работа в связке со строкой 11
        count = queryset.update(is_published=Women.Status.PUBLISHED) # count для подсчета сколько раз метод применялся, выводится в панель
        self.message_user(request, f'Изменено {count} записей') # вывод сколько записей было изменено

    @admin.action(description='Снять статью с публикации')  # декоратор для названия метода
    def set_draft(self, request, queryset):  # метод для того чтобы в действиях появилось собственное действие, работа в связке со строкой 11
        count = queryset.update(is_published=Women.Status.DRAFT)  # count для подсчета сколько раз метод применялся, выводится в панель
        self.message_user(request, f'{count} записей снято с публикации!', messages.WARNING)  # вывод сколько записей было изменено, WARNING для вывода знака внимание треугольничек

@admin.register(Category) # регистрация нашей модели, через декоратор
class CategoryAdmin(admin.ModelAdmin): # класс чтобы в админе отображались параметры женщин
    list_display = ('id', 'name') # отображение параметров из таблицы
    list_display_links = ('id', 'name') # чтобы при нажатиии мышкой отрывалось по названию, а не по id


# admin.site.register(Women, WomenAdmin)# регистрация нашей модели, 2й параметр, можно так или так @admin.register(Women)









