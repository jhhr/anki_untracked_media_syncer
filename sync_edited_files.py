import shutil
import time
from pathlib import Path

from aqt import mw

from .configuration import Config


def sync_edited_files():
    """
    Finds any files in the collection.media folder that have the _ prefix marking them
    untracked media files. Performs a file comparison to determine if the file has changed
    since last sync. If the file has changed, it will be renamed back and fort to trigger
    Anki to sync it.
    :return:
    """
    media_path = Path(mw.pm.profileFolder(), "collection.media")
    config = Config()
    config.load()
    sync_files = config.sync_files

    start_time = time.time()
    for file_name in sync_files.keys():
        file = media_path / file_name
        if file.is_dir() or not file.name.startswith("_"):
            continue

        new_file = file.with_name(file.name + "_temp")
        # Make sure the new file does not exist and keep trying until it doesn't
        while new_file.exists():
            new_file = new_file.with_name(new_file.name + "_")

        shutil.copy(file, new_file)
        shutil.move(new_file, file)

    print(f"Syncing files took {time.time() - start_time} seconds.")
