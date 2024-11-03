import logging
from colorama import Fore, Style, init
import os

# Инициализируем colorama
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        formatted_msg = super().format(record)

        # Применяем цвет ко всему сообщению в зависимости от уровня
        # Белый цвет для DEBUG и INFO
        color = Fore.LIGHTWHITE_EX
        if record.levelno == logging.WARNING:
            color = Fore.YELLOW
        elif record.levelno == logging.ERROR:
            color = Fore.RED
        elif record.levelno == logging.CRITICAL:
            color = Fore.MAGENTA

        return f"{color}{formatted_msg}{Style.RESET_ALL}"

class SimpleFormatter(logging.Formatter):
    def format(self, record):
        return super().format(record)

def log_startup_message(logger, message):
    logger.info(message)

log_path = os.path.join("log", "logs.log")
# Настройки логгера
logger = logging.getLogger("MonicaLogger")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(console_handler)
os.makedirs(os.path.dirname(log_path), exist_ok=True)
file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(SimpleFormatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(file_handler)

log_startup_message(logger, '-' * 30 + ' Начало работы программы ' + '-' * 30)