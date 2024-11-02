import pickle
import mmkv
import functional.sys_commands as sys_commands
import pyaudio
import json
from vosk import Model, KaldiRecognizer
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
        log.debug('создан объект класса VoiceListening')

    def start(self):
        self.stop_cycle = False
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.rec = KaldiRecognizer(self.model, 16000)
        self.listen()
        log.debug('отработала функция start, запуск цикла обработки голоса')

    def stop(self):
        self._stop_stream()
        self.stream.close()
        self.p.terminate()
        self.stop_cycle = True
        log.debug('остановка цикла обработки голоса')

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
        hotkey = []

        while not self.stop_cycle:
            if self.vc.operating_mode == 0:
                if not self.stream.is_active():
                    self.stream.start_stream()
                    log.debug('запущен поток модели')
                command = self.read_the_command()
                if command and command.lower().startswith(self.vc.keys["ultimate_key"]):
                    self.vc.command_recognition(command[len(self.vc.keys["ultimate_key"]) + 1:])
                if self.op_mod_1_active:
                    self.stop_thread()


            elif self.vc.operating_mode == 1:
                if not self.op_mod_1_active:
                    self.button_thread = threading.Thread(target=self.check_button)
                    self.button_thread.daemon = True
                    self.button_thread.start()
                    log.debug('запущен поток для клавиши переключения')
                    self.op_mod_1_active = True

                if self.switch_button_flag:
                    if not self.stream.is_active():
                        self.stream.start_stream()
                        log.debug('запущен поток модели')
                    self.vc.command_recognition(self.read_the_command())
                else:
                    if self.stream.is_active():
                        self._stop_stream()
                    time.sleep(0.1)

            elif self.vc.operating_mode == 2:
                if isinstance(self.vc.keys["switch_button"][0], str):
                    hotkey = keyboard.parse_hotkey(self.vc.keys["switch_button"][0])
                if all(keyboard.is_pressed(key) for key in hotkey):
                    last_press_time = time.time()  # Обновляем время последнего нажатия
                    print("Слушаю")
                    if not self.stream.is_active():
                        self.stream.start_stream()
                        log.debug('запущен поток модели')
                    while any(keyboard.is_pressed(key) for key in hotkey):
                        self.vc.command_recognition(self.read_the_command())
                        last_press_time = time.time()
                elif last_press_time is not None and (time.time() - last_press_time < listen_timeout):
                    self.vc.command_recognition(self.read_the_command())
                else:
                    self._stop_stream()
                    time.sleep(0.1)
                if self.op_mod_1_active:
                    self.stop_thread()

    def check_button(self):
        while not self.stop_button_thread:
            if isinstance(self.vc.keys["switch_button"][0], str):
                hotkey = keyboard.parse_hotkey(self.vc.keys["switch_button"][0])

                if all(keyboard.is_pressed(key) for key in hotkey):
                    self.switch_button_flag = not self.switch_button_flag
                    print("Слушаю" if self.switch_button_flag else "Не слушаю")

                    while any(keyboard.is_pressed(key) for key in hotkey):
                        time.sleep(0.1)
            time.sleep(0.01)

    def stop_thread(self):
        self.stop_button_thread = True
        self.button_thread.join()
        self.switch_button_flag = False
        self.op_mod_1_active = False
        log.debug('остановлен поток для клавиши переключения')

    def _stop_stream(self):
        if self.stream.is_active():
            while self.stream.get_read_available() > 0:
                self.stream.read(self.stream.get_read_available(), exception_on_overflow=False)
            self.stream.stop_stream()
            self.rec.Reset()
            log.debug('поток модели остановлен и очищен буфер')


class VoiceCommands:
    _instance = None
    kv = None
    _operating_mode = 0
    _keys = {
        "ultimate_key": ["моника"],
        "sound_key": ["звук"],
        "run_app_key": ["откр", "запус"],
        "media_player_keys": ["музык", "медиа"],
        "search_keys": ["гугл", "найди"],
        "switch_button": ["ctrl"],
        "hold_button": ["ctrl"]
    }

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
        if self.kv is not None:
            if 'operating_mode' not in self.kv:
                self._operating_mode = 1
                log.warning('Не удалось найти сохранённую переменную \"operating_mode\"')
            else:
                self._operating_mode = self.kv.getInt('operating_mode')
            if 'keys' not in self.kv:
                log.warning('Не удалось найти сохранённую переменную \"keys\"')
            else:
                self._keys = pickle.loads(self.kv.getBytes('keys'))
        else:
            log.error("Объект MMkv не найден")
        log.info('Объект класса \"VoiceCommands\" успешно создан')

    @property
    def keys(self):
        return self._keys

    @property
    def operating_mode(self):
        return self._operating_mode

    @keys.setter
    def keys(self, value):
        self._keys = value
        self.kv.set(value, 'keys')

    @operating_mode.setter
    def operating_mode(self, value):
        self._operating_mode = value
        self.kv.set(value, 'operating_mode')

    def command_recognition(self, command):
        if not command:
            return False
        if any(k in command for k in self._keys["sound_key"]):
            try:
                self.sound_commands(command)
            except Exception:
                log.warning("Говори по русски!", exc_info=True)
        elif any(k in command for k in self._keys["run_app_key"]):
            self.run_app_words(command)
        elif any(k in command for k in self._keys["media_player_keys"]):
            self.media_player(command)
        elif any(k in command for k in self._keys["search_keys"]):
            self.browser_search(command)

    def sound_commands(self, command):
        commands = {
            "word_set": any(kw in command for kw in ["устан"]),
            "word_up": any(kw in command for kw in ["увел", "выш"]),
            "word_down": any(kw in command for kw in ["меньш", "ниж"]),
            "word_off": any(kw in command for kw in ["выкл", "муть"]),
            "word_on": any(kw in command for kw in ["вклю", "раз"]),
            "word_na": "на" in command,
            "word_max": "макс" in command
        }

        value = None

        if commands["word_na"]:
            num_words = [word for word in command.split() if word in word_to_num]
            if len(num_words) == 1:
                value = word_to_num[num_words[0]]
            elif len(num_words) > 1:
                value = word_to_num[num_words[0] + ' ' + num_words[1]]
            if value is None:
                print('Уточните команду')
                return False

        if commands["word_set"] and value is not None:
            self.ac.volume_set(value)
        elif commands["word_up"] and value is not None:
            self.ac.volume_up(value)
        elif commands["word_up"]:
            self.ac.volume_up(5)
        elif commands["word_down"] and value is not None:
            self.ac.volume_down(value)
        elif commands["word_down"]:
            self.ac.volume_down(5)
        elif commands["word_on"]:
            self.ac.volume_on()
        elif commands["word_off"]:
            self.ac.volume_off()
        elif commands["word_max"]:
            self.ac.volume_max()
        elif commands["word_na"] and value is not None:
            self.ac.volume_set(value)
        else:
            print('Уточните команду')

    def run_app_word(self, command):
        word_count = 0
        split_command = command.split()
        for word in split_command:
            word_count += 1
            if word_count == 2:
                for key_word in self.app_man.paths.keys():
                    if key_word in word:
                        self.app_man.run_app(key_word)
                        return True
        log.debug('run_app_word не сработала, команда передана дальше')
        self.open_something(command)

    def run_app_words(self, command):
        for key_words in self.app_man.paths.keys():
            if key_words in command:
                self.app_man.run_app(key_words)
                return True
        log.debug('run_app_words не сработала, команда передана дальше')
        self.run_app_word(command)

    def open_something(self, command):
        word_count = 0
        second_word = None
        split_command = command.split()
        for word in split_command:
            word_count += 1
            if word_count == 2:
                second_word = word
                if 'провод' in word:
                    self.app_man.explorer()
                    return True
                elif 'кальк' in word:
                    self.app_man.calc()
                    return True
                elif 'настр' in word:
                    self.app_man.settings()
                    return True
        log.info(f'Не удалось открыть {second_word}')

    def media_player(self, command):
        play_pause = ['остан', 'продолж', 'вкл', 'выкл', 'пауз', 'плэй']
        for word in play_pause:
            if word in command:
                self._media.play_pause()
                return True
        if 'следущ' in command or 'некс' in command:
            self._media.next_track()
        elif 'предыдущ' in command or 'прошл' in command:
            self._media.previous_track()
        elif 'стоп' in command:
            self._media.stop()
        else:
            log.debug(f'media_player не распознала команду: {command}')
            print('Уточните команду для медиа')

    def browser_search(self, command):
        split_command = command.split()
        if split_command[0] == 'за':
            split_command.pop(0)
        split_command.pop(0)
        self.app_man.google_search(" ".join(split_command))


if __name__ == '__main__':
    monica = VoiceListening()
    monica.model = Model("../vosk-model-small-ru-0.22")
    monica.start()
