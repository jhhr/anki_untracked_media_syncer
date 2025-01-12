from aqt import mw

tag = mw.addonManager.addonFromModule(__name__)


def load_config():
    return mw.addonManager.getConfig(tag)


def save_config(data):
    mw.addonManager.writeConfig(tag, data)


class Config:
    def load(self):
        self.data = load_config()

    def save(self):
        save_config(self.data)

    @property
    def sync_files(self) -> dict[str, bool]:
        return self.data["sync_files"] or {}

    @sync_files.setter
    def sync_files(self, value: dict[str, bool]):
        self.data["sync_files"] = value

    @property
    def manage_dialog_shortcut(self) -> str:
        return self.data["manage_dialog_shortcut"] or "Ctrl+Alt+M"

    @manage_dialog_shortcut.setter
    def manage_dialog_shortcut(self, value: str):
        self.data["manage_dialog_shortcut"] = value
