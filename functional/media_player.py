import keyboard
from logger.logger_config import logger as log


class MediaPlayer:
    @staticmethod
    def play_pause():
        keyboard.send('play/pause media')
        log.info("Воспроизведение/Пауза")

    @staticmethod
    def next_track():
        keyboard.send('next track')
        log.info("Следующий трек")

    @staticmethod
    def previous_track():
        keyboard.send('previous track')
        log.info("Предыдущий трек")

    @staticmethod
    def stop():
        keyboard.send('stop media')
        log.info("Остановить воспроизведение")
