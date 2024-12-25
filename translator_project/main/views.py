from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, Template


# TODO реализовать логику консоли на jQuery
console = Template('''<div class="info">INFO: Запуск компиляции...</div>
	<div class="error">ERROR: Синтаксическая ошибка в строке 5</div>
	<div class="success">SUCCESS: Компиляция завершена успешно {{pages}}.</div>''')


def index(request):
    template_name = 'main/index.html'
    return render(request, template_name, context={'console': console.source})


def about(request):
    return HttpResponse('about.heml')
