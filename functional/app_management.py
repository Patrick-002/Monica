import subprocess
import pickle
import mmkv
import os
import sys
import configparser
import winshell
import webbrowser
import psutil
import win32process
import win32gui
from logger.logger_config import logger as log
from pathlib import Path


class AppManagement:
    _instance = None
    APP_ASSOCIATIONS = {
        '.txt': 'notepad',  # Открытие текстовых файлов в Блокноте
        '.docx': 'start winword',  # Открытие .docx в Microsoft Word
        '.pdf': 'start msedge',  # Открытие PDF в браузере Microsoft Edge
        '.jpg': 'start ms-photos:',  # Открытие изображений в приложении "Фотографии"
        '.jpeg': 'start ms-photos:',
        '.png': 'start ms-photos:',
        '.xlsx': 'start excel',  # Открытие Excel файлов в Microsoft Excel
        '.pptx': 'start powerpnt'  # Открытие презентаций в Microsoft PowerPoint
    }

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AppManagement, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.app_count = 1
        self.paths = {}
        self.kv = mmkv.MMKV.defaultMMKV()
        self.load_data()
        log.debug('создан объект класса AppManagement')

    def add_path(self, word: str, path: str):
        path = Path(path.replace('"', ''))
        if path.exists():
            if path.is_file() or path.is_dir():
                self.paths[word] = path.__str__()
                if self.kv is not None:
                    self.kv.set(pickle.dumps(self.paths), 'words')
                log.info(f'добавлен путь: {path.__str__()} на слово: {word}')
                return True
            else:
                log.error("Это объект другого типа, который мы не можем обработать")
                return False
        else:
            log.warning("Файл или папка не найдены")
            return False

    def edit_path(self, word_line_edit, path_line_edit):
        log.info(current_app())
        path = Path(path_line_edit.replace('"', ''))
        if word_line_edit in self.paths:
            if path.exists():
                if path.is_file() or path.is_dir():
                    self.paths[word_line_edit] = path_line_edit
                    self.kv.set(pickle.dumps(self.paths), 'words')
                    log.info(f"Путь для '{word_line_edit}' обновлен на '{path_line_edit}'")
                    return True
                else:
                    log.error("Это объект другого типа, который мы не можем обработать")
                    return False
            else:
                log.error("Файл по данному пути не существует")
                return False
        else:
            log.warning("Попытка изменить элемент не существующий в путях: \"" + word_line_edit + "\"")
            return False

    def delete_path(self, word):
        if word in self.paths:
            del self.paths[word]
            self.kv.set(pickle.dumps(self.paths), 'words')
            log.info(f"Элемент '{word}' удален")
            return True
        else:
            log.warning("Попытка удалить элемент не существующий в путях: \"" + word + "\"")
            return False

    def run_app(self, word: str):
        file_path = self.paths[word]
        file_extension = os.path.splitext(file_path)[1].lower()
        log.debug(f"run_app пытается запустить файл: {file_path}, с расширением {file_extension}")

        if file_extension == '.lnk':
            try:
                shortcut = winshell.Shortcut(file_path)
                target = shortcut.path
                if target:
                    subprocess.run([target])
                    print(f"Открыт ярлык {file_path}, который указывает на {target}")
                else:
                    print(f"Не удалось найти целевой файл для {file_path}")
            except Exception as e:
                log.warning(f"Ошибка при открытии ярлыка: {e}", exc_info=True)

        elif file_extension == '.exe':
            # Открываем .exe файл
            try:
                subprocess.Popen([file_path])
                log.info(f"Открыт исполняемый файл: {file_path}")
            except Exception as e:
                log.warning(f"Ошибка при открытии .exe файла: {e}", exc_info=True)

        elif file_extension == '.url':
            # Открываем .url интернет-ярлык
            try:
                config = configparser.ConfigParser()
                config.read(file_path)
                url = config['InternetShortcut']['URL']
                webbrowser.open(url)
                log.info(f"Открыт интернет-ярлык {file_path}, который указывает на {url}")
            except Exception as e:
                log.warning(f"Ошибка при открытии интернет-ярлыка: {e}", exc_info=True)

        elif any([k == file_extension for k in self.APP_ASSOCIATIONS.keys()]):
            app_command = self.APP_ASSOCIATIONS.get(file_extension)
            if app_command:
                try:
                    subprocess.Popen([app_command, file_path], shell=True)
                    log.info(f"Открыт файл {file_path}")
                except Exception as e:
                    log.warning(f"Ошибка при открытии файла: {e}", exc_info=True)
            else:
                log.info(f"Нет ассоциированного приложения для типа файла: {file_extension}")

        elif file_extension == '':
            if os.path.isdir(file_path):
                try:
                    subprocess.Popen(['explorer', file_path])
                    log.info(f"Открыта директория {file_path}")
                except Exception as e:
                    log.warning(f"Ошибка при открытии директории: {e}", exc_info=True)
            else:
                log.info(f"Файл без расширения не является директорией: {file_path}")
        else:
            log.warning(f"Неизвестный формат файла: {file_path}")

    def load_data(self):
        if self.kv is None:
            log.info(f"Ошибка инициализации MMKV.")
            return

        data = self.kv.getBytes('words')
        if data:
            self.paths = pickle.loads(data)


def current_app():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd == 0:
        log.error("Активное окно не найдено")
        return None
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    process = psutil.Process(pid)
    log.info("Текущее активное приложение: ", process)
    return process.name()

def explorer():
    log.debug('запускается проводник')
    subprocess.run(["explorer.exe"])

def calc():
    log.debug('запускается калькулятор')
    subprocess.run(["calc.exe"])

def settings():
    log.debug('открываются настройки')
    subprocess.run(["start", "ms-settings:"], shell=True)

def google_search(command):
    base_url = "https://www.google.com/search?q="
    search_url = base_url + command.replace(" ", "+")
    webbrowser.open(search_url)
    log.info(f"Ищем в Google: {command}")


