import functional.sys_commands  as sys_commands
import pyaudio
import json
from vosk import Model, KaldiRecognizer
from functional.text2numRUS import word_to_num
import functional.app_management as app_management

class VoiceController:
    # vosk-model-small-ru-0.22
    def __init__(self):
        self.model = Model("functional//vosk-model-small-ru-0.22")
        self.app_man = app_management.App_management()
        self.stream = None
        self.p = None
        self.rec = None
        self.ac = sys_commands.AudioController()
        self.stop_cycle = False
        self.sound_key_word = 'звук'
        self.run_app_key = 'запус'
        self.open_folder_key = 'откр'

    def rebind_key_word(self, key: str, word: str):
        if key == 'sound':
            self.sound_key_word = word

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
        if self.sound_key_word in command:
            self.sound_commands(command)
        if self.run_app_key in command:
            self.run_app_words(command)
        if self.open_folder_key in command:
            self.open_something(command)

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
                    if word in key_word or key_word in word:
                        self.app_man.run_app(key_word)
                        success = True
        if not success:
            print('Уточните команду')


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
            print('Уточните команду')

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


if __name__ == '__main__':
    monica = VoiceController()
    monica.start()
