import pickle
import mmkv
import functional.sys_commands as sys_commands
import pyaudio
import json
from vosk import Model, KaldiRecognizer, SetLogLevel
from functional.text_to_num_RUS import word_to_num
import functional.app_management as app_management
import functional.media_player as media_player
import keyboard
import time
import threading
from logger.logger_config import logger as log


class VoiceListening:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(VoiceListening, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        SetLogLevel(-1)
        self.model = Model("vosk-model-small-ru-0.22")
        self.stream = None
        self.p = None
        self.rec = None
        self.vc = VoiceCommands()
        self.stop_cycle = True
        self.switch_button_flag = False
        self.button_thread = None
        self.stop_button_thread = False
        self.op_mod_1_active = False

    def start(self):
        self.stop_cycle = False
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.rec = KaldiRecognizer(self.model, 16000)
        self.listen()
        log.debug('Запущен цикл обработки голоса')

    def stop(self):
        self._stop_stream()
        self.p.terminate()
        self.stop_cycle = True
        log.debug('Остановлен цикл обработки голоса')

    def read_the_command(self):
        data = self.stream.read(4000, exception_on_overflow=False)
        if self.rec.AcceptWaveform(data):
            command = json.loads(self.rec.Result())['text']
            if command:
                log.info(f"Распознано: {command}")
            return command or None

    def listen(self):
        listen_timeout = 5
        last_press_time = None

        while not self.stop_cycle:
            if self.vc.operating_mode == 0:
                self._handle_mode_0()
            elif self.vc.operating_mode == 1:
                self._handle_mode_1()
            elif self.vc.operating_mode == 2:
                last_press_time = self._handle_mode_2(listen_timeout, last_press_time)

    def activate_mode(self, mode):
        if mode != 1 and self.op_mod_1_active:
            self.stop_thread()

        if mode == 1:
            if not self.op_mod_1_active:
                self._start_button_thread()
            log.debug("Активирован режим 1")
        else:
            if self.op_mod_1_active:
                self.stop_thread()
            log.debug(f"Активирован режим {mode}")

    def _handle_mode_0(self):
        """Режим 0: Распознавание по ключевому слову"""
        self._start_stream_if_not_active()
        command = self.read_the_command()
        ultimate_keys = self.vc.keywords["ultimate_key"]
        for key in ultimate_keys:
            if command and command.lower().startswith(key):
                self.vc.command_recognition(command[len(key) + 1:])
                break
        if self.op_mod_1_active:
            self.stop_thread()

    def _handle_mode_1(self):
        """Режим 1: Использование кнопки для активации и деактивации прослушивания"""
        if not self.op_mod_1_active:
            self._start_button_thread()

        if self.switch_button_flag:
            self._start_stream_if_not_active()
            self.vc.command_recognition(self.read_the_command())
        else:
            self._stop_stream_if_active()
            time.sleep(0.1)

    def _handle_mode_2(self, listen_timeout, last_press_time):
        """Режим 2: Удержание кнопки для активации прослушивания"""
        if keyboard.is_pressed(self.vc.keys["hold_button"][0]):
            last_press_time = time.time()
            self._start_stream_if_not_active()
            print("Слушаю")
            while keyboard.is_pressed(self.vc.keys["hold_button"][0]):
                self.vc.command_recognition(self.read_the_command())
                last_press_time = time.time()
        elif last_press_time and (time.time() - last_press_time < listen_timeout):
            self.vc.command_recognition(self.read_the_command())
        else:
            self._stop_stream_if_active()
            time.sleep(0.1)
        if self.op_mod_1_active:
            self.stop_thread()
        return last_press_time

    def update_switch_button(self):
        if self.button_thread and self.button_thread.is_alive():
            self.stop_thread()
        self._start_button_thread()

    def check_button(self):
        while not self.stop_button_thread:
            if self.vc.operating_mode == 1:
                if keyboard.is_pressed(self.vc.keys["switch_button"][0]):
                    self.switch_button_flag = not self.switch_button_flag
                    print("Слушаю" if self.switch_button_flag else "Не слушаю")
                    while keyboard.is_pressed(self.vc.keys["switch_button"][0]):
                        time.sleep(0.1)
            time.sleep(0.01)

    def stop_thread(self):
        self.stop_button_thread = True
        if self.button_thread and self.button_thread.is_alive():
            self.button_thread.join()
            log.debug('Поток для кнопки завершен.')
        self.switch_button_flag = False
        self.op_mod_1_active = False
        self.stop_button_thread = False
        log.debug('Флаги сброшены.')

    def _start_stream_if_not_active(self):
        if not self.stream.is_active():
            self.stream.start_stream()
            log.debug('Запущен поток модели')

    def _stop_stream_if_active(self):
        if self.stream.is_active():
            self._stop_stream()

    def _start_button_thread(self):
        if not self.button_thread or not self.button_thread.is_alive():
            self.stop_button_thread = False
            self.button_thread = threading.Thread(target=self.check_button, daemon=True)
            self.button_thread.start()
            log.debug('Запущен новый поток для кнопки.')

    def _stop_stream(self):
        if self.stream.is_active():
            while self.stream.get_read_available() > 0:
                self.stream.read(self.stream.get_read_available(), exception_on_overflow=False)
            self.stream.stop_stream()
            self.rec.Reset()
            log.debug('Поток модели остановлен и очищен буфер')


class VoiceCommands:
    _instance = None
    _keywords_dict = {
        "ultimate_key": ["моника"],
        "sound_key": ["звук"],
        "run_app_key": ["откр", "запус"],
        "media_player_keys": ["музык", "медиа"],
        "search_keys": ["гугл", "найди"],
    }
    _keys_dict = {
        "switch_button": ["ctrl+a"],
        "hold_button": ["ctrl+a"]
    }
    _operating_mode = 0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(VoiceCommands, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.kv = mmkv.MMKV.defaultMMKV()
        self.ac = sys_commands.AudioController()
        self.app_man = app_management.AppManagement()
        self._media = media_player.MediaPlayer()
        self._load_configuration()
        log.info('Объект класса "VoiceCommands" успешно создан')

    def _load_configuration(self):
        if self.kv:
            if 'operating_mode' in self.kv:
                self._operating_mode = self.kv.getInt('operating_mode')
            else:
                log.warning(
                    'Не удалось найти сохранённую переменную "operating_mode", установлено значение по умолчанию - 0 (Распознавание по ключевому слову).')

            if 'keys' in self.kv:
                try:
                    self._keywords_dict = pickle.loads(self.kv.getBytes('keys'))
                except Exception as e:
                    log.error('Ошибка при загрузке ключей из MMKV, используются ключи по умолчанию.', exc_info=e)
            else:
                log.warning('Не удалось найти сохранённую переменную "_keywords_dict", используются ключи по умолчанию.')

            if 'binds' in self.kv:
                try:
                    self._keys_dict = pickle.loads(self.kv.getBytes('binds'))
                except Exception as e:
                    log.error('Ошибка при загрузке биндов из MMKV, используются ключи по умолчанию.', exc_info=e)
            else:
                log.warning('Не удалось найти сохранённую переменную "_keys_dict", используются ключи по умолчанию.')
        else:
            log.error("Объект MMKV не найден.")

    @property
    def keywords(self):
        return self._keywords_dict

    @property
    def keys(self):
        return self._keys_dict

    @keys.setter
    def keys(self, value):
        self._keys_dict = value
        if self.kv:
            try:
                self.kv.set(pickle.dumps(value), 'binds')
                log.info('Ключи успешно сохранены в MMKV.')
            except Exception as e:
                log.error('Ошибка при сохранении биндов в MMKV.', exc_info=e)
        else:
            log.error("Невозможно сохранить бинды, объект MMKV не найден.")

    def update_keywords(self, key, new_keywords_list):
        """Обновляет ключевые слова для заданного ключа и сохраняет в MMKV."""
        self._keywords_dict[key] = new_keywords_list
        if self.kv:
            try:
                self.kv.set(pickle.dumps(self._keywords_dict), 'keys')
                log.info('Ключевые слова успешно обновлены и сохранены в MMKV.')
            except Exception as e:
                log.error('Ошибка при сохранении обновленных ключевых слов в MMKV.', exc_info=e)
        else:
            log.error("Невозможно сохранить ключевые слова, объект MMKV не найден.")

    @keywords.setter
    def keywords(self, value):
        self._keywords_dict = value
        if self.kv:
            try:
                self.kv.set(pickle.dumps(value), 'keys')
                log.info('Ключи успешно сохранены в MMKV.')
            except Exception as e:
                log.error('Ошибка при сохранении ключей в MMKV.', exc_info=e)
        else:
            log.error("Невозможно сохранить ключи, объект MMKV не найден.")

    @property
    def operating_mode(self):
        return self._operating_mode

    @operating_mode.setter
    def operating_mode(self, value):
        self._operating_mode = value
        if self.kv:
            try:
                self.kv.set(value, 'operating_mode')
                log.debug(f'Режим работы {value} сохранён в MMKV.')
            except Exception as e:
                log.error('Ошибка при сохранении режима работы в MMKV.', exc_info=e)
        else:
            log.error("Невозможно сохранить режим работы, объект MMKV не найден.")

        voice_listener = VoiceListening()
        voice_listener.activate_mode(value)

    def command_recognition(self, command):
        if not command:
            return False

        command = command.lower()
        try:
            if any(keyword in command for keyword in self._keywords_dict["sound_key"]):
                self.sound_commands(command)
            elif any(keyword in command for keyword in self._keywords_dict["run_app_key"]):
                self.run_app_words(command)
            elif any(keyword in command for keyword in self._keywords_dict["media_player_keys"]):
                self.media_player(command)
            elif any(keyword in command for keyword in self._keywords_dict["search_keys"]):
                self.browser_search(command)
            else:
                log.debug(f"Не распознана команда: {command}")
        except Exception as e:
            log.error("Ошибка при обработке команды", exc_info=e)

    def sound_commands(self, command):
        commands = self.parse_command_flags(command)
        value = self.extract_volume_value(command) if commands.get("na") else None
        action_methods = {
            "set": self.ac.volume_set,
            "up": lambda v=None: self.ac.volume_up(v or 5),
            "down": lambda v=None: self.ac.volume_down(v or 5),
            "on": self.ac.volume_on,
            "off": self.ac.volume_off,
            "max": self.ac.volume_max,
        }

        for action, method in action_methods.items():
            if commands.get(action):
                if action in ["set", "up", "down"] and value is not None:
                    method(value)
                elif action in ["up", "down"] and value is None:
                    method()
                else:
                    method()
                return

        if commands.get("na") and value is not None:
            self.ac.volume_set(value)
        else:
            log.warning('Не удалось определить действие для звуковой команды.')
            print('Уточните команду')

    @staticmethod
    def parse_command_flags(command):
        return {
            "set": any(kw in command for kw in ["устан"]),
            "up": any(kw in command for kw in ["увел", "выш"]),
            "down": any(kw in command for kw in ["меньш", "ниж"]),
            "off": any(kw in command for kw in ["выкл", "муть"]),
            "on": any(kw in command for kw in ["вклю", "раз"]),
            "na": "на" in command,
            "max": "макс" in command
        }

    @staticmethod
    def extract_volume_value(command):
        num_words = [word for word in command.split() if word in word_to_num]
        if len(num_words) == 1:
            return word_to_num[num_words[0]]
        elif len(num_words) >= 2:
            combined = ' '.join(num_words[:2])
            return word_to_num.get(combined, word_to_num.get(num_words[0]))
        log.warning("Не удалось извлечь значение громкости из команды.")
        print('Уточните команду')
        return None

    def run_app_words(self, command):
        for key_word in self.app_man.paths:
            if key_word in command:
                self.app_man.run_app(key_word)
                log.info(f"Запущено приложение: {key_word}")
                return True
        log.debug('run_app_words не нашёл подходящего приложения, передача команды в run_app_word.')
        return self.run_app_word(command)

    def run_app_word(self, command):
        split_command = command.split()
        if len(split_command) >= 2:
            second_word = split_command[1]
            for key_word in self.app_man.paths:
                if key_word in second_word:
                    self.app_man.run_app(key_word)
                    log.info(f"Запущено приложение: {key_word}")
                    return True
            # Дополнительные приложения по ключевым словам
            fallback_actions = {
                'провод': app_management.explorer,
                'кальк': app_management.calc,
                'настр': app_management.settings
            }
            for keyword, action in fallback_actions.items():
                if keyword in second_word:
                    action()
                    log.info(f"Запущено действие: {keyword}")
                    return True
            log.info(f'Не удалось открыть приложение для слова: {second_word}')
        else:
            log.warning('Недостаточно слов в команде для запуска приложения.')
            print('Уточните команду')
        return False

    def media_player(self, command):
        if any(keyword in command for keyword in ['остан', 'продолж', 'вкл', 'выкл', 'пауз', 'плэй']):
            self._media.play_pause()
            return True
        elif any(keyword in command for keyword in ['следущ', 'некс']):
            self._media.next_track()
            return True
        elif any(keyword in command for keyword in ['предыдущ', 'прошл']):
            self._media.previous_track()
            return True
        elif 'стоп' in command:
            self._media.stop()
            return True
        else:
            log.debug(f'media_player не распознала команду: {command}')
            print('Уточните команду для медиа')
            return False

    @staticmethod
    def browser_search(command):
        split_command = command.split()
        if split_command[0] == 'за':
            split_command.pop(0)
        split_command.pop(0)
        app_management.google_search(" ".join(split_command))


if __name__ == '__main__':
    monica = VoiceListening()
    monica.model = Model("../vosk-model-small-ru-0.22")
    monica.start()
