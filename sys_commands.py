from pycaw.api.endpointvolume import IAudioEndpointVolume
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER


class AudioController:

    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()  # Получаем основное аудиоустройство (например, динамики или наушники)
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))

    def get_volume(self):
        current_volume = self.volume.GetMasterVolumeLevelScalar()
        return current_volume

    def set_system_volume(self, value: int):
        # Уровень громкости должен быть от 0.0 до 1.0
        value /= 100
        self.volume.SetMasterVolumeLevelScalar(value, None)

    def volume_up(self, value: int):
        value /= 100
        current_volume = self.get_volume()
        if current_volume + value > 1:
            self.volume.SetMasterVolumeLevelScalar(1, None)
        else:
            self.volume.SetMasterVolumeLevelScalar(current_volume + value, None)

    def volume_down(self, value: int):
        value /= 100
        current_volume = self.get_volume()
        if current_volume - value < 0:
            self.volume.SetMasterVolumeLevelScalar(0, None)
        else:
            self.volume.SetMasterVolumeLevelScalar(current_volume - value, None)

    def volume_off(self):
        self.volume.SetMute(1, None)

    def volume_on(self):
        self.volume.SetMute(0, None)

    def volume_max(self):
        self.volume.SetMasterVolumeLevelScalar(1, None)


if __name__ == "__main__":
    ac = AudioController()
    ac.set_system_volume(40)
    ac.volume_off()
    ac.volume_on()
    ac.volume_up(20)
    ac.volume_down(40)
