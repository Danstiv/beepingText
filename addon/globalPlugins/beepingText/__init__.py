import characterProcessing
import config
from globalPluginHandler import GlobalPlugin
from speech import commands, getCurrentLanguage, processText
from speech.extensions import pre_speechQueued

from .interface import add_settings, remove_settings

beep_command = commands.BeepCommand(150, 10)


class GlobalPlugin(GlobalPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_settings(self.on_save_config)
        pre_speechQueued.register(self.on_speech)

    def terminate(self):
        remove_settings()
        pre_speechQueued.unregister(self.on_speech)

    def on_speech(self, speechSequence):
        REPLACEMENT_MARKER = processText(
            getCurrentLanguage(),
            "---<replaced>---",
            characterProcessing.SymbolLevel(config.conf["speech"]["symbolLevel"]),
        )
        insertion_points = []
        for i, item in enumerate(speechSequence):
            # print(item)
            if not (isinstance(item, str) and item.startswith(REPLACEMENT_MARKER)):
                continue
            speechSequence[i] = item[len(REPLACEMENT_MARKER) :]
            insertion_points.append(i)
        for index in insertion_points[::-1]:
            speechSequence.insert(index, beep_command)

    def on_save_config(self):
        pass
