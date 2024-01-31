menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
]

class DataMixin: # это прописывается в классы представления обязательно первым параметром
    paginate_by = 5
    title_page = None # параметры, которые будут передаваться в основной класс представления
    cat_selected = None
    extra_context = {}

    def __init__(self): # иницианилизация с добавление в пустой словарь переменных для отправки в основной класс представления
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

    def get_mixin_context(self, context, **kwargs): # создаем словарь
        context['menu'] = menu # расширяем словарь стандартной информацией
        context['cat_selected'] = None #
        context.update(kwargs) # добаваляем содержимое из параметра **kwards
        return context


