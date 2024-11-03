import mmkv

from logger.logger_config import logger as log
from PySide6.QtWidgets import QWidget


class ThemeManager:
    _themes = ['dark', 'light', 'pink']
    _current_app_theme = 0

    def __init__(self):
        mmkv.MMKV.initializeMMKV(rootDir='.\\mmkv')
        self.kv = mmkv.MMKV.defaultMMKV()
        if self.kv:
            if 'current_app_theme' in self.kv:
                self._current_app_theme = self.kv.getInt('current_app_theme')
            else:
                log.info('Переменная current_app_theme не найдена, установлена тема по умолчанию')
        else:
            log.warning('Объект MMKV не найден, установлена тема по умолчанию')

    def apply_theme(self, widget: QWidget, theme: str = None):
        """
        Применяет выбранную тему к переданному виджету.

        :param widget: Виджет, к которому применяется стиль.
        :param theme: Название темы ('dark', 'light' или 'pink'). Если None, применяется текущая тема.
        """
        if theme is None:
            theme = self._themes[self._current_app_theme]

        style_file = f"UI/styles/{theme}_theme.qss"
        try:
            with open(style_file, "r") as file:
                style = file.read()
                widget.setStyleSheet(style)  # Применение стиля ко всему виджету
                log.info(f"Тема '{theme}' применена к '{widget.objectName()}'.")
        except FileNotFoundError:
            log.debug(f"Файл стиля '{style_file}' не найден.")

    def set_app_theme(self, theme_id: int):
        if 0 <= theme_id < len(self._themes):
            self._current_app_theme = theme_id
            if self.kv:
                try:
                    self.kv.set(theme_id, 'current_app_theme')
                    log.info(f'current_app_theme = {theme_id} сохранен в MMKV')
                except Exception as e:
                    log.error('Ошибка при сохранении темы!', exc_info=e)

        else:
            log.warning(f"Недопустимый индекс темы: {theme_id}.")

    def get_app_theme(self) -> str:
        return self._current_app_theme
