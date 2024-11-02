from pycaw.api.endpointvolume import IAudioEndpointVolume
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from logger.logger_config import logger as log


class AudioController:

    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()  # Получаем основное аудиоустройство (например, динамики или наушники)
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        log.debug('создан объект класса AudioController')

    def get_volume(self):
        current_volume = self.volume.GetMasterVolumeLevelScalar()
        return current_volume

    def volume_set(self, value: int):
        # Уровень громкости должен быть от 0.0 до 1.0
        value /= 100
        self.volume.SetMasterVolumeLevelScalar(value, None)
        log.debug(f'громкость установлена на {value * 100}')

    def volume_up(self, value: int):
        value /= 100
        current_volume = self.get_volume()
        if current_volume + value > 1:
            self.volume.SetMasterVolumeLevelScalar(1, None)
            log.debug(f'громкость установлена на 100')
        else:
            self.volume.SetMasterVolumeLevelScalar(current_volume + value, None)
            log.debug(f'громкость увеличена на {value * 100}')

    def volume_down(self, value: int):
        value /= 100
        current_volume = self.get_volume()
        if current_volume - value < 0:
            self.volume.SetMasterVolumeLevelScalar(0, None)
            log.debug(f'громкость установлена на 0')
        else:
            self.volume.SetMasterVolumeLevelScalar(current_volume - value, None)
            log.debug(f'громкость уменьшена на {value * 100}')

    def volume_off(self):
        self.volume.SetMute(1, None)
        log.debug(f'звук замучен')

    def volume_on(self):
        self.volume.SetMute(0, None)
        log.debug(f'звук размучен')

    def volume_max(self):
        self.volume.SetMasterVolumeLevelScalar(1, None)
        log.debug(f'громкость установлена на 100')
