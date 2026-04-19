import re

import characterProcessing
import config
from globalPluginHandler import GlobalPlugin
from speech import commands, getCurrentLanguage, processText
from speech.commands import PitchCommand
from speech.extensions import pre_speechQueued

from .interface import add_settings, remove_settings

beep_command = commands.BeepCommand(150, 10)
lower_pitch_command = PitchCommand(multiplier=0.3)
restore_pitch_command = PitchCommand()


def _generate_marker(raw_marker: str):
    return processText(
        getCurrentLanguage(),
        raw_marker,
        characterProcessing.SymbolLevel(config.conf["speech"]["symbolLevel"]),
    )


BEEP_REPLACEMENT_MARKER = _generate_marker("@replaced@")
LOWER_PITCH_MARKER = _generate_marker("@lower_pitch@")
RESTORE_PITCH_MARKER = _generate_marker("@restore_pitch@")
MARKERS_COMMANDS_MAP = {
    BEEP_REPLACEMENT_MARKER: beep_command,
    LOWER_PITCH_MARKER: lower_pitch_command,
    RESTORE_PITCH_MARKER: restore_pitch_command,
}
MARKER_REGEX = re.compile(
    "|".join(re.escape(marker) for marker in MARKERS_COMMANDS_MAP.keys())
)


class GlobalPlugin(GlobalPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add_settings(self.on_save_config)
        pre_speechQueued.register(self.on_speech)

    def terminate(self):
        # remove_settings()
        pre_speechQueued.unregister(self.on_speech)

    def on_speech(self, speechSequence):
        index = 0
        while index < len(speechSequence):
            item = speechSequence[index]
            if not (
                isinstance(item, str) and (matches := list(MARKER_REGEX.finditer(item)))
            ):
                index += 1
                continue
            items_to_insert = []
            offset = 0
            for match in matches:
                prefix, suffix = (item[offset : match.start()], item[match.end() :])
                offset = match.end()
                if prefix:
                    items_to_insert.append(prefix)
                items_to_insert.append(MARKERS_COMMANDS_MAP[match[0]])
            if suffix:
                items_to_insert.append(suffix)
            speechSequence[index] = items_to_insert.pop(0)
            index += 1
            for item_to_insert in items_to_insert:
                speechSequence.insert(index, item_to_insert)
                index += 1

    def on_save_config(self):
        pass
