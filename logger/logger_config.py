import logging
from colorama import Fore, Style, init
import os

# Инициализируем colorama
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        # Форматируем полное сообщение логгера
        formatted_msg = super().format(record)

        # Применяем цвет ко всему сообщению в зависимости от уровня
        if record.levelno == logging.WARNING:
            return f"{Fore.YELLOW}{formatted_msg}{Style.RESET_ALL}"
        elif record.levelno == logging.ERROR:
            return f"{Fore.RED}{formatted_msg}{Style.RESET_ALL}"
        elif record.levelno == logging.CRITICAL:
            return f"{Fore.MAGENTA}{formatted_msg}{Style.RESET_ALL}"
        else:
            # Белый цвет для DEBUG и INFO
            return f"{Fore.LIGHTWHITE_EX}{formatted_msg}{Style.RESET_ALL}"

class SimpleFormatter(logging.Formatter):
    def format(self, record):
        # Убираем цветовые коды и возвращаем обычный формат
        record.msg = record.getMessage()  # Просто получаем сообщение
        return super().format(record)

# Настройки логгера
logger = logging.getLogger("MonicaLogger")
logger.setLevel(logging.DEBUG)

# Формат сообщений
formatter = ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s')

# Консольный обработчик
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(console_handler)


def log_startup_message(message):
    # Создаём временный обработчик с простым форматом
    simple_formatter = logging.Formatter('%(message)s')
    temp_handler = logging.StreamHandler()
    temp_handler.setFormatter(simple_formatter)

    # Добавляем временный обработчик, выводим сообщение, затем удаляем обработчик
    logger.addHandler(temp_handler)
    logger.info(message)
    logger.removeHandler(temp_handler)

log_path = os.path.join("log", "logs.log")  # Создание директории и файла для логов
os.makedirs(os.path.dirname(log_path), exist_ok=True)  # Создаём директорию "log", если её нет
file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(SimpleFormatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
# Добавление файлового обработчика к логгеру
logger.addHandler(file_handler)

log_startup_message('-'*30 + 'Начало работы программы' + '-'*30)