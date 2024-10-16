import subprocess
import json
import os


class AppManagement:
    def __init__(self, filename="app_managment_data.json"):
        self.app_count = 1
        self.apps = {}
        self.folders = {}
        self.filename = filename
        if os.path.exists(self.filename):
            self.load_data()
        else:
            print('Файла нет')

    def explorer(self):
        subprocess.run(["explorer.exe"])

    def path(self):
        subprocess.run(["explorer.exe", self.path])

    def calc(self):
        subprocess.run(["calc.exe"])

    def settings(self):
        subprocess.run(["start", "ms-settings:"], shell=True)

    def add_folder_path(self, word: str, path: str):
        self.folders[word] = path
        self.save_data()

    def add_app_path(self, word: str, path: str):
        self.apps[word] = path
        self.save_data()

    def run_app(self, word: str):
        subprocess.run(self.apps[word])

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
        if os.path.getsize(self.filename) > 0:  # Проверка, что файл не пустой
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.apps = data.get("apps", {})
                self.folders = data.get("folders", {})
        else:
            print(f"{self.filename} пуст. Загружаем пустые словари.")
