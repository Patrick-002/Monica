from PySide6.QtCore import QFile
from PySide6.QtWidgets import QWidget


def apply_theme(widget: QWidget, theme: str):
    """
    Применяет выбранную тему к переданному виджету.

    :param widget: Виджет, к которому применяется стиль.
    :param theme: Название темы ('dark' или 'light').
    """
    style_file = f"UI/styles/{theme}_theme.qss"
    try:
        with open(style_file, "r") as file:
            style = file.read()
            widget.setStyleSheet(style)  # Применение стиля ко всему виджету
            print(f"Тема '{theme}' применена к '{widget.objectName()}'.")
    except FileNotFoundError:
        print(f"Файл стиля '{style_file}' не найден.")
