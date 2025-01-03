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

    @staticmethod
    def time_to_str():
        time_now = time.localtime(time.time())
        formst = time.strftime("%Y-%B-%d %H:%M:%S", time_now)
        return formst

    def __init__(self, status, message):
        self.time_now = ConsoleData.time_to_str()
        self.status = status
        self.message = message
    

        

# Инициализация TranslatorManager
api_url = "http://localhost:8000/translate"
translator = TranslatorManager(api_url=api_url)
console = []


def index(request):
    template_name = 'main/index.html'
    global console
    python_code = None
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            # Получаем Pascal-код из формы
            pascal_code = form.cleaned_data['text']
            
            # Добавляем задачу на перевод
            translator.add_task(pascal_code)
            print(translator)
            while not translator.queue_answers:
                print('wait')
                time.sleep(2)

            if translator.queue_answers:  # Если очередь не пуста, берем последний результат
                last_task = translator.queue_answers.popleft()

                if last_task.python_code:
                    console.append(ConsoleData(Status.success, last_task.info))
                    python_code = last_task.python_code

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

    return render(request, template_name, {'console': console, 'form': form, 'python_code': python_code})


def about(request):
    template_name = 'pages/about.html'
    return render(request, template_name)
