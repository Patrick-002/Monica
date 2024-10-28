import functional.sys_commands  as sys_commands
import pyaudio
import json
from vosk import Model, KaldiRecognizer
from functional.text2numRUS import word_to_num
import functional.appmanagement as app_management
import functional.media_player as media_player
import keyboard
import time

class VoiceController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(VoiceController, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # vosk-model-small-ru-0.22
    # vosk-model-ru-0.42
    def __init__(self):
        self.model = Model("functional//vosk-model-small-ru-0.22")
        # self.model = Model("functional//vosk-model-ru-0.42")
        self.stream = None
        self.p = None
        self.rec = None
        self.ac = sys_commands.AudioController()
        self.app_man = app_management.AppManagement()
        self.media = media_player.MediaPlayer()
        self.cycle = True
        self.ultimate_key = 'моника'
        self.sound_key = 'звук'
        self.run_app_key = 'запус'
        self.open_folder_key = 'откр'
        self.media_player_key_1 = 'музык'
        self.media_player_key_2 = 'медиа'
        self.search_key_1 = 'гугл'
        self.search_key_2 = 'найди'
        self.switch_button_flag = False
        self.switch_button = 'ctrl'
        self.hold_button = 'ctrl'
        self.operating_mode = 2
        # 1 - авто по self.ultimate_key; 2 - переключение по self.switch_button; 3 - зажатие на self.hold_button


    def start(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.rec = KaldiRecognizer(self.model, 16000) # Инициализируем распознаватель
        self.listen()

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.cycle = False

    def read_the_command(self):
        data = self.stream.read(4000)
        if self.rec.AcceptWaveform(data):
            command = json.loads(self.rec.Result())['text']
            print(f"Распознано: {command}")
            if command:
                return command
            else:
                return None

    def listen(self):
        while self.cycle:
            if self.operating_mode == 1:
            # Режим постоянного прослушивания, но выполняется только если команда начинается с self.ultimate_key
                if not self.stream.is_active():
                    self.stream.start_stream()
                command = self.read_the_command()
                if command:
                    if command.lower().startswith(self.ultimate_key):
                        command = command[len(self.ultimate_key) + 1:]
                        print(f'Передаю: {command}')
                        self.command_recognition(command)

            elif self.operating_mode == 2: # Режим переключения прослушивания кнопкой
                if keyboard.is_pressed(self.switch_button):
                    self.switch_button_flag = not self.switch_button_flag
                    print("Слушаю" if self.switch_button_flag else "Не слушаю")
                    while keyboard.is_pressed(self.switch_button):
                        pass  # Ждем, пока кнопка будет отпущена
                if self.switch_button_flag:
                    if not self.stream.is_active():
                        self.stream.start_stream()
                    self.command_recognition(self.read_the_command())
                elif not self.switch_button_flag:
                    if self.stream.is_active():
                        while self.stream.get_read_available() > 0:
                            self.stream.read(self.stream.get_read_available(), exception_on_overflow=False)
                        self.stream.stop_stream()  # Останавливаем поток, чтобы не было overflow
                        self.rec.Reset()
                    time.sleep(0.1)  # Пауза, чтобы не нагружать процессор

            elif self.operating_mode == 3:
                if keyboard.is_pressed(self.hold_button):
                    print('Слушаю')
                    if not self.stream.is_active():
                        self.stream.start_stream()
                    while keyboard.is_pressed(self.hold_button):
                        self.command_recognition(self.read_the_command())
                else:
                    if self.stream.is_active():
                        while self.stream.get_read_available() > 0:
                            self.stream.read(self.stream.get_read_available(), exception_on_overflow=False)
                        self.stream.stop_stream()
                        self.rec.Reset()
                    time.sleep(0.1)

    def command_recognition(self, command):
        if not command:
            return False
        if self.sound_key in command:
            try:
                self.sound_commands(command)
            except Exception as e:
                print('Говори по русски!')
        elif self.run_app_key in command:
            self.run_app_words(command)
        elif self.open_folder_key in command:
            self.open_something(command)
        elif self.media_player_key_1 in command or self.media_player_key_2 in command:
            self.media_player(command)
        elif self.search_key_1 in command or self.search_key_2 in command:
            self.browser_search(command)

    def sound_commands(self, command):
        split_command = command.split()
        value = None
        word_set = False
        word_up = False
        word_down = False
        word_off = False
        word_on = False
        word_na = False
        word_max = False
        # for word in split_command:
        if 'устан' in command:
            word_set = True
        if 'увел' in command or 'выш' in command:
            word_up = True
        if 'меньш' in command or 'ниж' in command:
            word_down = True
        if 'выкл' in command or 'муть' in command:
            word_off = True
        if 'вклю' in command or 'раз' in command:
            word_on = True
        if 'на' in command:
            word_na = True
        if 'макс' in command:
            word_max = True

        if word_na:
            word_count = 0
            num_word = ''
            for word in split_command:
                if word_count == 1 and word in word_to_num:
                    num_word += ' '
                    num_word += word
                    break
                if word in word_to_num:
                    num_word += word
                    word_count += 1
            value = word_to_num[num_word]
            if not value:
                print('Уточните команду')
                return False
        if word_set and word_na:
            self.ac.volume_set(value)
        elif word_up and word_na:
            self.ac.volume_up(value)
        elif word_up:
            self.ac.volume_up(5)
        elif word_down and word_na:
            self.ac.volume_down(value)
        elif word_down:
            self.ac.volume_down(5)
        elif word_on:
            self.ac.volume_on()
        elif word_off:
            self.ac.volume_off()
        elif word_max:
            self.ac.volume_max()
        elif word_na:
            self.ac.volume_set(value)
        else:
            print('Уточните команду')

    def run_app_word(self, command):
        success = False
        word_count = 0
        split_command = command.split()
        for word in split_command:
            word_count += 1
            if word_count == 2:
                for key_word in self.app_man.paths.keys():
                    if key_word in word:
                        self.app_man.run_app(key_word)
                        success = True
        if not success:
            print('Уточните команду для приложения')

    def run_app_words(self, command):
        success = False
        for key_words in self.app_man.paths.keys():
            if key_words in command:
                self.app_man.run_app(key_words)
                success = True
        if not success:
            self.run_app_word(command)

    def open_folder(self, word):
        success = False
        for key_word in self.app_man.paths.keys():
            if word in key_word:
                self.app_man.open_folder(key_word)
                success = True
        if not success:
            print('Уточните команду для папки')

    def open_something(self, command):
        word_count = 0
        split_command = command.split()
        for word in split_command:
            word_count += 1
            if word_count == 2:
                if 'провод' in word:
                    self.app_man.explorer()
                elif 'кальк' in word:
                    self.app_man.calc()
                elif 'настр' in word:
                    self.app_man.settings()
                else:
                    self.open_folder(word)

    def media_player(self, command):
        play_pause = ['остан', 'продолж', 'вкл', 'выкл', 'пауз', 'плэй']
        for word in play_pause:
            if word in command:
                self.media.play_pause()
                return True
        if 'следущ' in command or 'некс' in command:
            self.media.next_track()
        elif 'предыдущ' in command or 'прошл' in command:
            self.media.previous_track()
        elif 'стоп' in command:
            self.media.stop()
        else:
            print('Уточните команду для медиа')

    def browser_search(self, command):
        split_command = command.split()
        if split_command[0] == 'за':
            split_command.pop(0)
        split_command.pop(0)
        self.app_man.google_search(" ".join(split_command))


if __name__ == '__main__':
    monica = VoiceController()
    monica.start()
