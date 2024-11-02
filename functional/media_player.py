import keyboard
from logger.logger_config import logger as log


class MediaPlayer:
    def play_pause(self):
        keyboard.send('play/pause media')
        log.info("Воспроизведение/Пауза")

    def next_track(self):
        keyboard.send('next track')
        log.info("Следующий трек")

    def previous_track(self):
        keyboard.send('previous track')
        log.info("Предыдущий трек")

    def stop(self):
        keyboard.send('stop media')
        log.info("Остановить воспроизведение")
