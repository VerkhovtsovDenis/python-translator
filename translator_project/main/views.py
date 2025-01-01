from django.shortcuts import render
from django.http import HttpResponse
from .forms import TextForm
from .Mediator import TranslatorManager  # Импорт модуля Mediator
import time
from dataclasses import dataclass
from enum import Enum


Status = Enum('status', [('success', 1), ('error', 2), ('info', 3)])

@dataclass
class ConsoleData:
    time_now: str
    status: Enum
    message: str

    def __init__(self, status, message):
        self.time_now = str(time.strftime("%Y-%B-%d %H:%M:%S", time.localtime(time.time())))
        self.status = status
        self.message = message
        

# Инициализация TranslatorManager
api_url = "http://localhost:8000/translate"
translator = TranslatorManager(api_url=api_url, max_queue_size=10)
console = []



def index(request):
    template_name = 'main/index.html'
    global console

    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            # Получаем Pascal-код из формы
            pascal_code = form.cleaned_data['text']
            
            # Добавляем задачу на перевод
            translator.add_task(pascal_code)
            
            # Ждем выполнения задачи (можно оптимизировать с помощью асинхронности)
            time.sleep(2)  # Увеличить время, если необходимо

            # Проверяем результат обработки
            if translator.queue:  # Если очередь не пуста, берем последний результат
                last_task = translator.queue[-1]
                if last_task.python_code:
                    console.append(ConsoleData(Status.success, last_task.python_code))
                elif last_task.errors:
                    console.append(ConsoleData(Status.error, last_task.errors))
                else:
                    console.append(ConsoleData(Status.info, 'Перевод в процессе...'))

            else:
                console.append(ConsoleData(Status.info, 'Очередь пуста, задача обрабатывается'))
        else:
            # TODO - недостижимый код, при невалидности формы post запрос не будет сгенерирован
            console.append(ConsoleData(Status.error, 'Форма невалидна.'))
    else:
        form = TextForm()

    return render(request, template_name, {'console': console, 'form': form})


def about(request):
    template_name = 'pages/about.html'
    return render(request, template_name)
