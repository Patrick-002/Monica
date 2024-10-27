import subprocess
import pickle
import mmkv
import json
import os
import configparser
import winshell
import webbrowser


class AppManagement:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AppManagement, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.app_count = 1
        self.paths = {}
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
        kv = mmkv.MMKV.defaultMMKV()
        kv.set(pickle.dumps(self.paths), 'words')

    def run_app(self, word: str):
        subprocess.run(self.paths[word])
        file_path = self.apps[word]
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
        subprocess.run(self.folders[word])

    def save_data(self):
        data = {
            "apps": self.apps,
            "folders": self.folders
        }
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        kv = mmkv.MMKV.defaultMMKV()
        file = kv.getBytes('words')
        if len(file) == 0:
            print("Файл пуст. Загружаем пустые словари.")
            return
        self.paths =  pickle.loads(file)

    def google_search(self, command):
        base_url = "https://www.google.com/search?q="
        search_url = base_url + command.replace(" ", "+")
        webbrowser.open(search_url)

        print(f"Ищем в Google: {command}")
