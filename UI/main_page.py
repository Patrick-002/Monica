from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QSizePolicy, QVBoxLayout, QLabel
from sys_commands import AudioController


class MainPage(QWidget):
    def __init__(self, page_manager):
        super().__init__()

        self.page_manager = page_manager  # Сохраняем экземпляр PageManager
        self.page_manager.register_page(self.__class__.__name__, self)

        layout = QVBoxLayout()
        self.ac = AudioController()  # Инициализация контроллера звука
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()

        button_style = """
        QPushButton {
            background-color: rgb(85, 170, 255);
            color: white;
            border-radius: 10px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: rgb(100, 180, 255);
        }
        """

        # Стиль для текстового поля
        text_box_style = """
        QLineEdit {
            background-color: lightyellow;  /* Цвет фона */
            color: darkblue;                /* Цвет текста */
            font-size: 16px;                /* Размер текста */
            border: 2px solid gray;         /* Толщина и цвет границы */
            border-radius: 5px;             /* Радиус скругления углов */
        }
        """

        # Создаем текстовое поле для ввода громкости
        self.volume_input_box = QLineEdit(self)
        self.volume_input_box.setPlaceholderText("Введите громкость (0-100)")
        self.volume_input_box.setStyleSheet(text_box_style)  # Применяем стиль

        # Устанавливаем политику размеров
        self.volume_input_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Кнопка для установки громкости
        self.set_volume_button = QPushButton('Set Volume')
        self.set_volume_button.setStyleSheet(button_style)
        self.set_volume_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.set_volume_button.clicked.connect(self.volume_set)  # Привязываем обработчик события

        # Остальные кнопки
        self.volume_up_button = QPushButton('Volume Up')
        self.volume_up_button.setStyleSheet(button_style)
        self.volume_up_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.volume_up_button.clicked.connect(self.volume_up)  # Привязываем обработчик события

        self.volume_down_button = QPushButton('Volume Down')
        self.volume_down_button.setStyleSheet(button_style)
        self.volume_down_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.volume_down_button.clicked.connect(self.volume_down)  # Привязываем обработчик события

        self.volume_off_button = QPushButton('Mute')
        self.volume_off_button.setStyleSheet(button_style)
        self.volume_off_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.volume_off_button.clicked.connect(self.volume_off)  # Привязываем обработчик события

        self.volume_on_button = QPushButton('Unmute')
        self.volume_on_button.setStyleSheet(button_style)
        self.volume_on_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.volume_on_button.clicked.connect(self.volume_on)  # Привязываем обработчик события

        # Добавляем виджеты в сетку
        layout.addWidget(self.volume_input_box, 0, 0, 1, 2)  # Растягиваем на 2 колонки
        layout.addWidget(self.set_volume_button, 1, 0, 1, 2)

        layout.addWidget(self.volume_up_button, 2, 0)
        layout.addWidget(self.volume_down_button, 2, 1)
        layout.addWidget(self.volume_off_button, 3, 0)
        layout.addWidget(self.volume_on_button, 3, 1)

        # Устанавливаем растяжение для строк и столбцов
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

        # Устанавливаем минимальные отступы (margins) для всего layout
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(40)

        # Устанавливаем сетку в качестве основного layout
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
        self.page_manager.show_page('SettingsPage')

    def volume_max(self):
        print('Установлена максимальная громкость!')
        self.ac.volume_max()
