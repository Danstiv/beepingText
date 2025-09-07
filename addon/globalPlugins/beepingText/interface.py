import addonHandler
import config
import gui.guiHelper

from .interface_helpers import ConfigBoundSettingsPanel, bind_with_config

addonHandler.initTranslation()


class BeepingTextSettingsPanel(ConfigBoundSettingsPanel):
    title = addonHandler.getCodeAddon().manifest["summary"]

    def makeSettings(self, settings_sizer):
        self.config = config.conf["beepingText"]
        # sizer = gui.guiHelper.BoxSizerHelper(self, sizer=settings_sizer)


def add_settings(on_save_callback):
    BeepingTextSettingsPanel.on_save_callback = on_save_callback
    gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(
        BeepingTextSettingsPanel
    )


def remove_settings():
    gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(
        BeepingTextSettingsPanel
    )
