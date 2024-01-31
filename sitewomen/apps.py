from django.apps import AppConfig


class SitewomenConfig(AppConfig):
    verbose_name = 'Женщины мира' # чтобы в кабинете админа загололвок был как нужно нам
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sitewomen'
