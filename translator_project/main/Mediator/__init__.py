from dataclasses import dataclass
from collections import deque
import requests
from threading import Thread, Lock
from typing import Optional
import logging


@dataclass
class CodeToken:
    pascal_code: str
    python_code: Optional[str] = None
    info: Optional[str] = None
    errors: Optional[str] = None


class TranslatorManager:
    def __init__(self, api_url: str, max_queue_size: int = 10):
        self.api_url = api_url
        self.queue = deque(maxlen=max_queue_size)
        self.active = True  # Флаг активности
        self.lock = Lock()
        self.worker_thread = Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

        logging.basicConfig(
            filename="translator.log",
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        logging.debug("TranslatorManager initialized.")

    def stop(self):
        """Завершение обработки задач."""
        self.active = False
        self.worker_thread.join()
        logging.info("TranslatorManager stopped.")

    def _process_queue(self):
        while self.active or self.queue:
            task: Optional[CodeToken] = None

            with self.lock:
                if self.queue:
                    task = self.queue.popleft()

            if task:
                logging.debug(f"Processing task: {task.pascal_code}")
                self._translate(task)

    def add_task(self, pascal_code: str):
        with self.lock:
            if len(self.queue) < self.queue.maxlen:
                self.queue.append(CodeToken(pascal_code=pascal_code))
                logging.info(f"Task added. Queue size: {len(self.queue)}/" +
                             f"{self.queue.maxlen}")
            else:
                logging.warning("Queue is full. Task rejected.")

    def _translate(self, task: CodeToken):
        logging.debug('start debugging')
        try:
            logging.debug(f"Translation are start translate code: {task}")

            response = requests.post(
                self.api_url,
                json={
                    "pascal_code": task.pascal_code,
                    "target_language": 'python'
                },
                timeout=1000
            )
            print(response.status_code)
            logging.debug(f"Translation are get response: {response}")

            response.raise_for_status()
            task.python_code = response.json().get('result_code')
            task.errors = response.json().get('errors')

            task.info = "Translation successful."
            
            logging.info(f"Translation complete: \t {task.python_code}, \n {task.errors}")

        except requests.RequestException as ex:
            task.errors = str(ex)
            task.info = "Translation failed."
            logging.error(f"Error during translation: {task.errors}")
        except Exception as other_ex:
            task.errors = str(other_ex)
            task.info = "Translation failed."
            logging.error(f"Error during translation: {task.errors}")


if __name__ == '__main__':
    api_url = "http://localhost:8000/translate"
    translator = TranslatorManager(api_url=api_url)

    pascal_code = "program aaa var i, j: real; b: string; begin i := 1.9 " + \
                  "+ 0.1; writeln(i); end."
    translator.add_task(pascal_code)

    # Дождаться завершения обработки
    import time
    time.sleep(2)  # Небольшая задержка для выполнения задач
    translator.stop()  # Корректное завершение
