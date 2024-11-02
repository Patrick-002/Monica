from logger.logger_config import logger as log
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QWidget

themes = ['dark', 'light', 'pink']
current_app_theme: str = themes[0]


def apply_theme(widget: QWidget, theme: str = current_app_theme):
    """
    Применяет выбранную тему к переданному виджету.

    :param widget: Виджет, к которому применяется стиль.
    :param theme: Название темы ('dark', 'light' или 'pink').
    """
    style_file = f"UI/styles/{theme}_theme.qss"
    try:
        with open(style_file, "r") as file:
            style = file.read()
            widget.setStyleSheet(style)  # Применение стиля ко всему виджету
            log.info(f"Тема '{theme}' применена к '{widget.objectName()}'.")
    except FileNotFoundError:
        log.debug(f"Файл стиля '{style_file}' не найден.")


def set_app_theme(theme_id: int):
    global current_app_theme
    current_app_theme = themes[theme_id]


def get_app_theme_id():
    global current_app_theme
    return current_app_theme
