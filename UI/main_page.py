from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from sys_commands import AudioController


class MonicaUI(QWidget):
    def __init__(self):
        super().__init__()

        self.ac = AudioController()
        self.setWindowTitle('Monica Assistant')
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Создаем текстовое поле для ввода громкости
        self.volume_input_box = QLineEdit(self)
        self.volume_input_box.setPlaceholderText("Введите громкость (0-100)")
        layout.addWidget(self.volume_input_box)

        # Кнопка для установки громкости
        self.set_volume_button = QPushButton('Set Volume')
        self.set_volume_button.clicked.connect(self.volume_set)
        layout.addWidget(self.set_volume_button)

        # Остальные кнопки
        self.volume_up_button = QPushButton('Volume Up')
        self.volume_up_button.clicked.connect(self.volume_up)
        layout.addWidget(self.volume_up_button)

        self.volume_down_button = QPushButton('Volume Down')
        self.volume_down_button.clicked.connect(self.volume_down)
        layout.addWidget(self.volume_down_button)

        self.volume_off_button = QPushButton('Mute')
        self.volume_off_button.clicked.connect(self.volume_off)
        layout.addWidget(self.volume_off_button)

        self.volume_on_button = QPushButton('Unmute')
        self.volume_on_button.clicked.connect(self.volume_on)
        layout.addWidget(self.volume_on_button)

        self.setLayout(layout)

    def volume_on(self):
        print("Звук включен!")
        self.ac.volume_on()

    def volume_up(self):
        volume_value = self.volume_input_box.text()
        if volume_value == '':
            volume_value = 5
        volume_value = int(volume_value)
        print(f"Громкость повышена на {volume_value}!")
        self.ac.volume_up(volume_value)

    def volume_down(self):
        volume_value = self.volume_input_box.text()
        if volume_value == '':
            volume_value = 5
        volume_value = int(volume_value)
        print(f"Громкость понижена на {volume_value}!")
        self.ac.volume_down(volume_value)

    def volume_set(self):
        volume_value = self.volume_input_box.text()
        if volume_value == '':
            print("Пожалуйста, введите значение от 0 до 100.")
            return False
        volume_value = int(volume_value)
        if 0 <= volume_value <= 100:
            print(f"Громкость установлена на: {volume_value}%")
            self.ac.volume_set(volume_value)
        else:
            print("Пожалуйста, введите значение от 0 до 100.")

    def volume_off(self):
        print("Звук выключен!")
        self.ac.volume_off()

    def volume_max(self):
        print('Установлена максимальная громкость!')
        self.ac.volume_max()