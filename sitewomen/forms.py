from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from .models import Category, Husband, Women


class AddPostForm(forms.ModelForm): # создаем форму на классе forms.Form
    '''
    данные поля оставляем здесь чтобы на странице можно было в них поместить выбор
    '''
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категории:') # empty_label= прописывает внутри блока на странице то если пользователь пока не выбрал
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label='Не за мужем', label='Муж:')

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags2'] # отображает поля которые в модели по умолчанию все поля, кроме которые заполняются автоматически
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }
        labels = {'slug': 'URL'}

    def clean_title(self):  # собственный валидатор метод чтобы в поле выводилась своё указание на ошибку вводимой информации
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title

class UploadFileForm(forms.Form): # форма непривязанная к модели для загрузки файла на сервер - проверка валидности файла
    # file = forms.FileField(label='Файл')
    file = forms.ImageField(label='Файл') # можно и так, по умолчанию идет выбор из папки файлов именно картинки, но для этого нужен пакет pillow


    # title = forms.CharField(max_length=255,
    #                         min_length=5,
    #                         widget=forms.TextInput(attrs={'class': 'form-input'}), # widget - как будет выглядеть на странице это поле
    #                         label='Заголовок:',
    #                         error_messages={ # это самостоятельный обработчик ошибок
    #                             'min_length': 'Слишком короткий заголовок',
    #                             'required': 'Без заголовка никак'
    #                         })
    # slug = forms.SlugField(max_length=255, label='URL:')
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Контент:') # required=False параметр необязательно
    # is_published = forms.BooleanField(required=False, initial=True, label='Статус:') # для чекбокса по умолчанию выбрано
    # cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категории:') # empty_label= прописывает внутри блока на странице
    # husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label='Не за мужем', label='Муж:')

    # def clean_title(self): # собственный валидатор метод чтобы в поле выводилась своё указание на ошибку вводимой информации
    #     title = self.cleaned_data['title']
    #     ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦШЩЬЪЫЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя1234567890- '
    #
    #     if not (set(title) <= set(ALLOWED_CHARS)):
    #         raise ValidationError('Должны присутствовать только русские символы, дефис и пробел.')

