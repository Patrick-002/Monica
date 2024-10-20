from os.path import split

import functional.sys_commands  as sys_commands
import pyaudio
import json
from vosk import Model, KaldiRecognizer
from functional.text2numRUS import word_to_num
import functional.appmanagement as app_management
import functional.media_player as media_player

class VoiceController:
    # vosk-model-small-ru-0.22
    # vosk-model-ru-0.42
    def __init__(self):
        self.model = Model("functional//vosk-model-small-ru-0.22") # functional//model
        self.stream = None
        self.p = None
        self.rec = None
        self.ac = sys_commands.AudioController()
        self.app_man = app_management.AppManagement()
        self.media = media_player.MediaPlayer()
        self.stop_cycle = False
        self.sound_key = 'звук'
        self.run_app_key = 'запус'
        self.open_folder_key = 'откр'
        self.media_player_key_1 = 'музык'
        self.media_player_key_2 = 'медиа'
        self.search_key_1 = 'гугл'
        self.search_key_2 = 'найди'

    def rebind_key_word(self, key: str, word: str):
        if key == 'sound_key':
            self.sound_key = word
        elif key == 'run_app_key':
            self.run_app_key = word
        elif key == 'open_folder_key':
            self.open_folder_key = word
        elif key == 'media_player_key_1':
            self.media_player_key_1 = word
        elif key == 'media_player_key_2':
            self.media_player_key_2 = word
        elif key == 'search_key_1':
            self.search_key_1 = word
        elif key == 'search_key_2':
            self.search_key_2 = word

    def start(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.stream.start_stream()
        # Инициализируем распознаватель
        self.rec = KaldiRecognizer(self.model, 16000)

        while True:
            data = self.stream.read(4000)
            if self.rec.AcceptWaveform(data):
                command = json.loads(self.rec.Result())['text']
                print(f"Распознано: {command}")
                self.command_recognition(command)
                if self.stop_cycle:
                    break

    def command_recognition(self, command):
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

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.stop_cycle = True

    def run_app_word(self, command):
        success = False
        word_count = 0
        split_command = command.split()
        for word in split_command:
            word_count += 1
            if word_count == 2:
                for key_word in self.app_man.apps.keys():
                    if key_word in word:
                        self.app_man.run_app(key_word)
                        success = True
        if not success:
            print('Уточните команду для приложения')


    def run_app_words(self, command):
        success = False
        for key_words in self.app_man.apps.keys():
            if key_words in command:
                self.app_man.run_app(key_words)
                success = True
        if not success:
            self.run_app_word(command)

    def open_folder(self, word):
        success = False
        for key_word in self.app_man.folders.keys():
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
        play_pause = ['остан','продолж','вкл','выкл','пауз','плэй']
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
