This addon will automatically sync untracked (prefixed with _) media files that have been edited
since last sync.

Normally merely editing an untracked file will not cause it to be synced. One trick is to rename it back and forth, causing it be identified as a new file.

# How to use

- Install addon
- Open the dialog from the main window > Tools > Untracked Media Sync
- In the **Files** table, click on files to move them to **Files to sync**. Click again to move them back.
- Click **Save** to store these selections as the files that will be synced.

Whenever you edit your files, Sync in Anki to upload the changes to AnkiWeb

## How it works

- Whenever you sync in Anki, all the selected files will be copied in place so that Anki thinks they're new files.
- There is no tracking of which files have been edited. All selected files are uploaded to AnkiWeb on every sync, replacing their previous versions.

# Recommendation

- Use this for a few files that you edit frequently. For example, javascript files that you import in your templates, some JSONs you use as data for addons/templates.
- Don't set particularly large files to be auto-synced as this will make every sync take longer and waste AnkiWeb bandwith as the big files get uploaded every time...


## Possible conflicts, if you edit in two places at once before syncing

The first to sync and upload to Ankiweb wins - those files will be downloade and overwrite the others as you sync on other devices.
