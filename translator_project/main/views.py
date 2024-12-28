from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, Template
from .forms import TextForm

# TODO реализовать логику консоли на jQuery
console = '''<div class="info">INFO: Запуск компиляции...</div>
    <div class="error">ERROR: Синтаксическая ошибка в строке 5</div>
    <div class="success">SUCCESS: Компиляция завершена успешно {{pages}}.</div>'''


def index(request, methods=["POST", "GET"]):
    global console

    template_name = 'main/index.html'
    if request.method == "POST":

        form = TextForm(request.POST)
        if form.is_valid():
            console += form.cleaned_data['text']
    else:
        form = TextForm()

    return render(request, template_name, {'console': console, "form": form})


def about(request):
    return HttpResponse('about.heml')
