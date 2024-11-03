from pycaw.api.endpointvolume import IAudioEndpointVolume
from pycaw.pycaw import AudioUtilities
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from logger.logger_config import logger as log


class AudioController:
    MAX_VOLUME = 1.0
    MIN_VOLUME = 0.0
    PERCENT_CONVERSION_FACTOR = 100.0

    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()  # Получаем основное аудиоустройство (например, динамики или наушники)
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        log.debug('Создан объект класса AudioController')

    @property
    def current_volume(self) -> float:
        return self.volume.GetMasterVolumeLevelScalar() * self.PERCENT_CONVERSION_FACTOR

    @current_volume.setter
    def current_volume(self, value: float):
        if not (self.MIN_VOLUME <= value <= self.PERCENT_CONVERSION_FACTOR):
            log.error(f'Значение громкости {value} вне допустимого диапазона (0-100)')
            return
        scalar_value = value / self.PERCENT_CONVERSION_FACTOR
        self.volume.SetMasterVolumeLevelScalar(scalar_value, None)
        log.debug(f'Громкость установлена на {value:.2f}%')

    def volume_set(self, value: int):
        log.debug(f'Устанавливаю громкость на {value}%')
        self.current_volume = value

    def volume_up(self, increment: int = 5):
        new_volume = min(self.current_volume + increment, self.PERCENT_CONVERSION_FACTOR)
        self.current_volume = new_volume
        log.debug(f'Громкость увеличена, новая громкость: {new_volume:.2f}%')

    def volume_down(self, decrement: int = 5):
        new_volume = max(self.current_volume - decrement, self.MIN_VOLUME)
        self.current_volume = new_volume
        log.debug(f'Громкость уменьшена, новая громкость: {new_volume:.2f}%')

    def volume_off(self):
        self.volume.SetMute(1, None)
        log.debug('Звук выключен')

    def volume_on(self):
        self.volume.SetMute(0, None)
        log.debug('Звук включен')

    def volume_max(self):
        self.current_volume = self.PERCENT_CONVERSION_FACTOR
        log.debug('Громкость установлена на 100%')