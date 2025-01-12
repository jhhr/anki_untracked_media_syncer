import os
import sys
from aqt.gui_hooks import sync_will_start
from aqt.qt import QAction, qconnect

from aqt import mw

from .sync_edited_files import sync_edited_files
from .media_sync_dialog import open_media_sync_dialog
from .configuration import Config

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))

sync_will_start.append(sync_edited_files)


def build_action(fun, text, shortcut=None):
    """
    :param: fun - the function to be called when the action is triggered
    :param: text - the text in the menu
    :param: shortcut - the shortcut to trigger the action
    """
    action = QAction(text)
    action.triggered.connect(lambda b, did=None: fun(did))
    if shortcut:
        action.setShortcut(shortcut)
    return action


config = Config()
config.load()

action_mw = QAction("Untracked Media Sync", mw)
action_mw.setShortcut(config.manage_dialog_shortcut)
qconnect(action_mw.triggered, open_media_sync_dialog)
mw.form.menuTools.addAction(action_mw)
