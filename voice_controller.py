import os
import re
from os.path import split
import sys_commands

import pyaudio
import json
from vosk import Model, KaldiRecognizer
from text2numRUS import word_to_num


class VoiceController:
    # vosk-model-small-ru-0.22
    def __init__(self):
        self.model = Model("vosk-model-small-ru-0.22")
        self.stream = None
        self.p = None
        self.ac = sys_commands.AudioController()

    def start(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.stream.start_stream()
        # Инициализируем распознаватель
        rec = KaldiRecognizer(self.model, 16000)

        while True:
            data = self.stream.read(4000)
            if rec.AcceptWaveform(data):
                command = json.loads(rec.Result())['text']
                print(f"Распознано: {command}")
                if not self.execute_command(command):
                    self.stop()
                    break

    def execute_command(self, command):
        split_command = command.split()
        value = None
        word_volume = False
        word_set = False
        word_up = False
        word_down = False
        word_off = False
        word_on = False
        stop = False
        word_na = False
        word_max = False
        for word in split_command:
            if 'громк' in word:
                word_volume = True
            if 'устан' in word:
                word_set = True
            if 'увел' in word:
                word_up = True
            if 'уменьш' in word:
                word_down = True
            if 'выкл' in word or 'муть' in word:
                word_off = True
            if 'вклю' in word or 'раз' in word:
                word_on = True
            if 'стоп' in word:
                stop = True
            if 'на' in word:
                word_na = True
            if 'макс' in word:
                word_max = True

        if stop:
            self.stop()
            return False
        if word_na:
            for word in split_command:
                if word in word_to_num:
                    value = word_to_num[word]
                    break
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
        elif word_volume and word_na:
            self.ac.volume_set(value)

        return True

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


if __name__ == '__main__':
    monica = VoiceController()
    monica.start()
