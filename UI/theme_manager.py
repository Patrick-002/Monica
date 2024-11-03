import mmkv
from logger.logger_config import logger as log
from PySide6.QtWidgets import QWidget
import os


class ThemeManager:
    _themes = ['dark', 'light', 'pink']
    _current_app_theme = 0
    _style_cache = {}

    def __init__(self):
        mmkv.MMKV.initializeMMKV(rootDir='.\\mmkv')
        self.kv = mmkv.MMKV.defaultMMKV()
        if self.kv:
            if 'current_app_theme' in self.kv:
                self._current_app_theme = self.kv.getInt('current_app_theme')
            else:
                log.info('Переменная current_app_theme не найдена, установлена тема по умолчанию')
        else:
            log.warning('Не удалось инициализировать MMKV. Используется тема по умолчанию')

    def apply_theme(self, widget: QWidget, theme: str = None):
        """
        Применяет выбранную тему к переданному виджету, его родителям и всем дочерним элементам рекурсивно.
        """
        theme = theme or self._themes[self._current_app_theme]
        style = self._load_style(theme)

        if style:
            current_widget = widget
            while current_widget is not None:
                current_widget.setStyleSheet(style)
                current_widget = current_widget.parentWidget()
            widget.setStyleSheet(style)
            for child in widget.findChildren(QWidget):
                child.setStyleSheet(style)
            log.info(f"Тема '{theme}' применена рекурсивно к '{widget.objectName()}' и его родительским элементам.")
        else:
            log.error(f"Не удалось применить тему '{theme}': файл стиля отсутствует.")

    def _load_style(self, theme: str) -> str:
        if theme in self._style_cache:
            return self._style_cache[theme]

        return self._load_style_from_file(theme) or self._load_style_from_fallbacks(theme)

    def _load_style_from_file(self, theme: str):
        style_file = f"UI/styles/{theme}_theme.qss"
        if os.path.exists(style_file):
            try:
                with open(style_file, "r") as file:
                    style = file.read()
                    self._style_cache[theme] = style
                    return style
            except Exception as e:
                log.error(f"Ошибка при загрузке файла стиля '{style_file}': {e}")
        return None

    def _load_style_from_fallbacks(self, theme: str) -> str:
        for fallback_theme in self._themes:
            if fallback_theme != theme:
                style = self._load_style_from_file(fallback_theme)
                if style:
                    log.info(f"Стиль '{fallback_theme}' успешно загружен как резервный.")
                    return style
        log.error("Не удалось найти ни одного файла стиля для всех тем.")
        return ""

    def set_app_theme(self, theme_id: int):
        """
        Устанавливает идентификатор темы приложения и сохраняет его в хранилище MMKV.
        """
        if 0 <= theme_id < len(self._themes):
            self._current_app_theme = theme_id
            if self.kv:
                try:
                    self.kv.set(theme_id, 'current_app_theme')
                    log.info(f'current_app_theme = {theme_id} сохранен в MMKV')
                except Exception as e:
                    log.error("Ошибка при сохранении темы в MMKV.", exc_info=e)
            else:
                log.warning("Объект MMKV не найден. Тема не сохранена.")
        else:
            log.warning(f"Недопустимый индекс темы: {theme_id}.")

    def get_app_theme(self) -> str:
        """
        Возвращает текущую тему приложения.
        """
        return self._themes[self._current_app_theme]
