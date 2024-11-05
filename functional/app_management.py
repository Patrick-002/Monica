import subprocess
import pickle
import mmkv
import os
import webbrowser
import psutil
import win32process
import win32gui
from logger.logger_config import logger as log
from pathlib import Path
from urllib.parse import urlparse


class AppManagement:
    _instance = None
    APP_ASSOCIATIONS = {
        '.txt': 'notepad',              # Открытие текстовых файлов в Блокноте
        '.docx': 'start winword',       # Открытие .docx в Microsoft Word
        '.pdf': 'start msedge',         # Открытие PDF в браузере Microsoft Edge
        '.jpg': 'start ms-photos:',     # Открытие изображений в приложении "Фотографии"
        '.jpeg': 'start ms-photos:',
        '.png': 'start ms-photos:',
        '.xlsx': 'start excel',         # Открытие Excel файлов в Microsoft Excel
        '.pptx': 'start powerpnt'       # Открытие презентаций в Microsoft PowerPoint
    }

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.paths = {}
        self.kv = mmkv.MMKV.defaultMMKV()
        self._load_data()
        log.debug('Создан экземпляр класса AppManagement')

    def add_path(self, keyword: str, path: str) -> bool:
        path_obj = Path(path.strip('"'))
        if self._path_exists(path_obj) or is_url(path):
            self.paths[keyword] = str(path_obj)
            self._save_data()
            log.info(f'Добавлено значение: {path_obj} для ключа: {keyword}')
            return True

        log.warning("Файл или папка не найдены")
        return False

    def edit_path(self, keyword: str, path: str) -> bool:
        path_obj = Path(path.strip('"'))
        if keyword in self.paths and self._path_exists(path_obj):
            self.paths[keyword] = str(path_obj)
            self._save_data()
            log.info(f"Путь для '{keyword}' обновлен на '{path_obj}'")
            return True
        log.warning(f"Попытка изменить несуществующий путь для ключа '{keyword}'")
        return False

    @staticmethod
    def _path_exists(path: Path) -> bool:
        return path.exists() and (path.is_file() or path.is_dir())

    def _save_data(self):
        if self.kv is not None:
            self.kv.set(pickle.dumps(self.paths), 'paths')

    def delete_path(self, keyword: str) -> bool:
        if keyword in self.paths:
            del self.paths[keyword]
            self._save_data()
            log.info(f"Элемент '{keyword}' удален")
            return True
        log.warning(f"Попытка удалить несуществующий элемент: '{keyword}'")
        return False

    def run_app(self, keyword: str):
        file_path = self.paths.get(keyword)
        if not file_path:
            log.error(f"Ключ '{keyword}' не найден в сохраненных путях.")
            return

        log.debug(f"Попытка запустить файл: {file_path}")
        try:
            if os.path.isdir(file_path):
                subprocess.Popen(['explorer', file_path])
            else:
                file_extension = os.path.splitext(file_path)[1].lower()
                app_command = self.APP_ASSOCIATIONS.get(file_extension)
                if app_command:
                    subprocess.run([app_command, file_path], shell=True)
                else:
                    os.startfile(file_path)
        except Exception as e:
            log.error(f"Ошибка при запуске '{file_path}': {e}", exc_info=True)

    def _load_data(self):
        if self.kv is None:
            log.error("Ошибка инициализации MMKV.")
            return
        data = self.kv.getBytes('paths')
        if data:
            try:
                self.paths = pickle.loads(data)
                log.debug("Данные загружены из MMKV.")
            except (pickle.PickleError, TypeError) as e:
                log.error(f"Ошибка при загрузке данных: {e}")

def current_app() -> str:
    hwnd = win32gui.GetForegroundWindow()
    if hwnd == 0:
        log.error("Активное окно не найдено")
        return ""
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    process = psutil.Process(pid)
    log.info(f"Текущее активное приложение: {process.name()}")
    return process.name()

def explorer():
    log.debug('Запуск проводника')
    subprocess.run(["explorer.exe"])

def calc():
    log.debug('Запуск калькулятора')
    subprocess.run(["calc.exe"])

def settings():
    log.debug('Открытие настроек')
    subprocess.run(["start", "ms-settings:"], shell=True)

def google_search(query: str):
    base_url = "https://www.google.com/search?q="
    search_url = base_url + query.replace(" ", "+")
    webbrowser.open(search_url)
    log.info(f"Ищем в Google: {query}")

def is_url(string: str) -> bool:
    parsed = urlparse(string)
    return all([parsed.scheme, parsed.netloc])