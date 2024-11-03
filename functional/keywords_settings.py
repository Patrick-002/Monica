import keyboard
from logger.logger_config import logger as log
from functional.voice_controller import VoiceCommands



class KeywordsSettings:
    def __init__(self):
        self.vc = VoiceCommands()

    def get_key_combination(self):
        print("Нажмите любую клавишу или комбинацию...")
        keys_pressed = set()

        while True:
            event = keyboard.read_event(suppress=True)

            if event.event_type == keyboard.KEY_DOWN:
                keys_pressed.add(event.name)

            elif event.event_type == keyboard.KEY_UP:
                if len(keys_pressed) > 1:
                    combination = "+".join(keys_pressed)
                    log.info(f"Нажата комбинация: {combination}")
                    return combination
                else:
                    key = keys_pressed.pop()
                    log.info(f"Нажата клавиша: {key}")
                    return key

            keys_pressed.clear()

    def rebind_vc_keys(self, key):
        key_pressed = self.get_key_combination()
        self.vc.keys[key][0] = key_pressed

    def add_vc_keywords(self, key, new_keyword:str):
        self.vc.keys[key].append(new_keyword)

    def rebind_vc_keywords(self, key, new_keyword:str, index):
        self.vc.keys[key][index] = new_keyword