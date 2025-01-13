from pathlib import Path

from aqt.gui_hooks import sync_will_start
from aqt import mw


def sync_edited_files():
    media_path = Path(mw.pm.profileFolder(), "collection.media")
    # bump mtime in folder to trigger sync of any edited files
    media_path.touch()


sync_will_start.append(sync_edited_files)
