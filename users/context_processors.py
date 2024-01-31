'''
для того чтобы передавать общие которые нужны на всех страницах данные на страницу, чтобы не повторялся код в каждом классе пердставления
'''
from sitewomen.utils import menu

def get_women_context(request): # далее нужно оязательно в settings в TEMPLATES в context_proccesors прописать 'users.context_processors.get_women_context',
    return {'mainmenu': menu}
