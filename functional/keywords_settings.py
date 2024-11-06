import keyboard
from logger.logger_config import logger as log
from functional.voice_controller import VoiceCommands
from PySide6.QtCore import Signal, QObject


class KeywordsSettings(QObject):
    keys_updated = Signal()  # Сигнал для обновления списка ключей

    def __init__(self):
        super().__init__()  # Инициализация базового класса
        self.vc = VoiceCommands()

    def get_key_combination(self):
        """Ожидание ввода клавиши или комбинации клавиш от пользователя."""
        print("Нажмите любую клавишу или комбинацию...")
        keys_pressed = set()

        while True:
            event = keyboard.read_event(suppress=True)

            if event.event_type == keyboard.KEY_DOWN and event.name == 'esc':
                log.info("Отмена ввода клавиши")
                return None

            if event.event_type == keyboard.KEY_DOWN:
                keys_pressed.add(event.name)

            elif event.event_type == keyboard.KEY_UP:
                if keys_pressed:  # Проверяем, есть ли клавиши в наборе
                    if len(keys_pressed) > 1:
                        combination = "+".join(keys_pressed)
                        log.info(f"Нажата комбинация: {combination}")
                        return combination
                    else:
                        key = keys_pressed.pop()  # Удаляем клавишу из набора
                        log.info(f"Нажата клавиша: {key}")
                        return key
                # Если keys_pressed пустой, просто игнорируем событие отпускания клавиши

    def rebind_vc_keys(self, key):
        """Изменить комбинацию клавиш для голосовой команды."""
        if key in self.vc.keys:  # Проверяем, существует ли ключ
            key_pressed = self.get_key_combination()
            if key_pressed is None:
                return
            updated_keys = self.vc.keys
            updated_keys[key][0] = key_pressed
            self.vc.keys = updated_keys
            log.info(f"Комбинация для ключа {key} успешно изменена на {key_pressed}")
            self.keys_updated.emit()  # Вызываем сигнал, чтобы обновить ключи
        else:
            log.error(f"Ключ {key} не найден в keywords")

    def add_vc_keywords(self, key, new_keyword: str):
        """Добавить новое ключевое слово к голосовой команде."""
        if key in self.vc.keywords:  # Проверяем, существует ли ключ
            updated_keywords = self.vc.keywords[key]
            updated_keywords.append(new_keyword)
            self.vc.update_keywords(key, updated_keywords)  # Сохраняем изменения
            log.info(f"Добавлено новое ключевое слово '{new_keyword}' для ключа '{key}'")
            self.keys_updated.emit()  # Вызываем сигнал, чтобы обновить ключи
        else:
            log.error(f"Ключ {key} не найден в keywords")

    def rebind_vc_keywords(self, key, new_keyword: str, index):
        """Перепривязка ключевого слова по индексу."""
        if key in self.vc.keywords and index < len(self.vc.keywords[key]):
            updated_keywords = self.vc.keywords[key]
            updated_keywords[index] = new_keyword
            self.vc.update_keywords(key, updated_keywords)  # Сохраняем изменения
            log.info(f"Ключевое слово для {key} обновлено на {new_keyword} по индексу {index}")
            self.keys_updated.emit()  # Вызываем сигнал, чтобы обновить ключи
        else:
            log.error(f"Ключ {key} не найден или индекс {index} вне диапазона для keywords")

    def remove_vc_keywords(self, key, index):
        if key in self.vc.keywords and index < len(self.vc.keywords[key]):
            updated_keywords = self.vc.keywords.copy()
            del updated_keywords[key][index]
            self.vc.update_keywords(updated_keywords)
            log.info(f"Ключевое слово для {key} удалено по индексу {index}")
            self.keys_updated.emit()  # Вызываем сигнал, чтобы обновить ключи
        else:
            log.error(f"Ключ {key} не найден или индекс {index} вне диапазона для keywords")