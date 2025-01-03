from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PascalCodeFrom
from .Mediator import TranslatorManager, CodeToken  # Импорт модуля Mediator
import time
from dataclasses import dataclass
from enum import Enum
from .models import History
from typing import List

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
console: List[ConsoleData] = []

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return str(ip)


def index(request):
    template_name = 'main/index.html'
    global console
    python_code = str()

    if request.method == "POST":
        my_task = CodeToken()

        form = PascalCodeFrom(request.POST)

        if form.is_valid():
            pascal_code = form.cleaned_data['pascal_code']
            translator.add_task(pascal_code)

            new_tiket = History.objects.create(
                ip_address=get_client_ip(request=request),
                pascal_code=pascal_code,
            )
            while not translator.queue_answers:
                print('wait')
                time.sleep(2)

            if translator.queue_answers:
                my_task: CodeToken = translator.queue_answers.popleft()

                if my_task.python_code:
                    console.append(ConsoleData(Status.success, my_task.info))
                    new_tiket.python_code = my_task.python_code
                elif my_task.errors:
                    console.append(ConsoleData(Status.error, my_task.errors))
                    new_tiket.translating_errors = my_task.errors
                else:
                    console.append(ConsoleData(Status.info, 'Перевод в процессе...'))
            else:
                console.append(ConsoleData(Status.info, 'Очередь пуста, задача обрабатывается'))
            
            new_tiket.save()
            print(f'Данные должны были быть сохранены: {new_tiket}')

        else:
            console.append(ConsoleData(Status.error, 'Форма невалидна.'))
    else:
        form = PascalCodeFrom()

    return render(request, template_name, {'console': console, 'form': form, 'python_code': python_code})


def about(request):
    template_name = 'pages/about.html'
    return render(request, template_name)

def history(request):
    template_name = 'main/history.html'
    
    history = History.objects.all()
    print(*history)

    return render(request, template_name, {'history': history})

def history_del(request):
    # Удалить все объекты из модели History
    History.objects.all().delete()
    # Перенаправить на страницу истории
    return redirect('/history/', permanent=True)
