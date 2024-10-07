from pycaw.api.endpointvolume import IAudioEndpointVolume
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

class audio_commands():
    devices = AudioUtilities.GetSpeakers()  # Получаем основное аудиоустройство (например, динамики или наушники)
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    def get_volume(self):
        current_volume = audio_commands.volume.GetMasterVolumeLevelScalar()
        return current_volume


    def set_system_volume(self, level):
        # Уровень громкости должен быть от 0.0 до 1.0
        audio_commands.volume.SetMasterVolumeLevelScalar(level, None)


    # Пример использования: установить громкость на 50% (0.5)
    set_system_volume(0.5)