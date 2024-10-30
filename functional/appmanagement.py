import subprocess
import pickle
from mmkv import SingleProcess
import mmkv
import os
import configparser
import winshell
import webbrowser


class AppManagement:
    _instance = None
    kv = None

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
        mmkv.MMKV.initializeMMKV('./mmkv')
        self.kv = mmkv.MMKV.defaultMMKV(SingleProcess)
        self.load_data()

    def explorer(self):
        subprocess.run(["explorer.exe"])

    def path(self):
        subprocess.run(["explorer.exe", self.path])

    def calc(self):
        subprocess.run(["calc.exe"])

    def settings(self):
        subprocess.run(["start", "ms-settings:"], shell=True)

    def add_path(self, word: str, path: str):
        self.paths[word] = path
        if self.kv is not None:
            self.kv.set(pickle.dumps(self.paths), 'words')

    def edit_path(self, word_line_edit, path_line_edit):
        if word_line_edit in self.paths:
            self.paths[word_line_edit] = path_line_edit
            self.kv.set(pickle.dumps(self.paths), 'words')
            print(f"Путь для '{word_line_edit}' обновлен на '{path_line_edit}'")

    def delete_path(self, word):
        if word in self.paths:
            del self.paths[word]
            self.kv.set(pickle.dumps(self.paths), 'words')
            print(f"Элемент '{word}' удален")

    def run_app(self, word: str):
        file_path = self.paths[word]
        file_extension = os.path.splitext(file_path)[1].lower()

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
                print(f"Ошибка при открытии ярлыка: {e}")

        elif file_extension == '.exe':
            # Открываем .exe файл
            try:
                subprocess.Popen([file_path])
                # print(f"Открыт исполняемый файл: {file_path}")
            except Exception as e:
                print(f"Ошибка при открытии .exe файла: {e}")

        elif file_extension == '.url':
            # Открываем .url интернет-ярлык
            try:
                config = configparser.ConfigParser()
                config.read(file_path)
                url = config['InternetShortcut']['URL']
                webbrowser.open(url)
                print(f"Открыт интернет-ярлык {file_path}, который указывает на {url}")
            except Exception as e:
                print(f"Ошибка при открытии интернет-ярлыка: {e}")

        else:
            print(f"Неизвестный формат файла: {file_path}")

    def open_folder(self, word: str):
        subprocess.run(self.paths[word])

    def load_data(self):
        if self.kv is None:
            print("Ошибка инициализации MMKV.")
            self.paths = {}  # Устанавливаем пустой словарь, если MMKV не работает
            return

        data = self.kv.getBytes('words')
        if data:
            self.paths = pickle.loads(data)
        else:
            self.paths = {}  # Задаем пустой словарь по умолчанию

    def google_search(self, command):
        base_url = "https://www.google.com/search?q="
        search_url = base_url + command.replace(" ", "+")
        webbrowser.open(search_url)

        print(f"Ищем в Google: {command}")
