import keyboard

class MediaPlayer:
    def play_pause(self):
        keyboard.send('play/pause media')
        print("Воспроизведение/Пауза")

    def next_track(self):
        keyboard.send('next track')
        print("Следующий трек")

    def previous_track(self):
        keyboard.send('previous track')
        print("Предыдущий трек")

    def stop(self):
        keyboard.send('stop media')
        print("Остановить воспроизведение")