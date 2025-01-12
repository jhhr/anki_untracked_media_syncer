from pathlib import Path
from aqt import mw
from aqt.qt import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QToolTip,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    Qt,
    QPushButton,
    QTimer,
)
from .configuration import Config


class MediaSyncDialog(QDialog):
    def __init__(self, parent=None, sync_files: dict[str, bool] = {}):
        super().__init__(parent)
        self.sync_files = sync_files

        self.setWindowTitle("Media Sync")
        self.resize(800, 400)

        self.layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search files...")
        self.search_timer = QTimer(self)
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.filter_files)
        self.search_bar.textChanged.connect(self.start_search_timer)
        search_layout.addWidget(self.search_bar)

        self.layout.addLayout(search_layout)

        tables_layout = QHBoxLayout()

        self.unselected_table = QTableWidget(self)
        self.unselected_table.setColumnCount(1)
        self.unselected_table.setHorizontalHeaderLabels(["Files"])
        self.unselected_table.horizontalHeader().setStretchLastSection(True)
        self.unselected_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.unselected_table.itemClicked.connect(self.select_file)
        tables_layout.addWidget(self.unselected_table)

        self.selected_table = QTableWidget(self)
        self.selected_table.setColumnCount(1)
        self.selected_table.setHorizontalHeaderLabels(["Files to sync"])
        self.selected_table.horizontalHeader().setStretchLastSection(True)
        self.selected_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.selected_table.itemClicked.connect(self.deselect_file)
        tables_layout.addWidget(self.selected_table)

        self.layout.addLayout(tables_layout)

        # Cancel button
        self.cancel_button = QPushButton("Close without saving", self)
        self.cancel_button.clicked.connect(self.reject)
        # Close button
        self.close_button = QPushButton("Save", self)
        self.close_button.clicked.connect(self.accept)
        hbox = QHBoxLayout()
        hbox.addWidget(self.cancel_button)
        hbox.addWidget(self.close_button)
        self.layout.addLayout(hbox)

        self.setLayout(self.layout)

    def start_loading(self):
        QToolTip.showText(
            self.unselected_table.mapToGlobal(self.unselected_table.rect().topLeft()),
            "<p>Loading files... This may take a while, if you have a lot of media files</p>",
            widget=self,
            rect=self.unselected_table.rect(),
            # We'll use a long show time, so that the tooltip will show while the files are loading
            # except, if there's enough files for the loading to take more than this
            msecShowTime=30000,
        )
        # Run timers sequentially so that that the tooltip has time to render too
        # 50ms seems enough here too
        QTimer.singleShot(50, self.load_files)

    def showEvent(self, event):
        # Runs when the dialog is shown
        super().showEvent(event)
        # 50ms seems like enough for the dialog to render, less than this and the tooltip
        # sometimes gets cut off at the top a bit
        QTimer.singleShot(50, self.start_loading)

    def load_files(self):
        media_path = Path(mw.pm.profileFolder(), "collection.media")
        self.files = [
            file.name
            for file in media_path.iterdir()
            if file.is_file() and file.name.startswith("_")
        ]
        # Hide the tooltip, if it's still showing
        QToolTip.hideText()
        self.populate_tables()

    def populate_tables(self):
        self.unselected_table.setRowCount(len(self.files) - len(self.sync_files))
        self.selected_table.setRowCount(len(self.sync_files))

        unselected_row_index = 0
        selected_row_index = 0

        for file_name in self.files:
            file_item = QTableWidgetItem(file_name)
            file_item.setFlags(file_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            if file_name in self.sync_files:
                self.selected_table.setItem(selected_row_index, 0, file_item)
                selected_row_index += 1
            else:
                self.unselected_table.setItem(unselected_row_index, 0, file_item)
                unselected_row_index += 1

        # Set table header to show number of files
        self.unselected_table.setHorizontalHeaderLabels([f"Files ({unselected_row_index})"])
        self.selected_table.setHorizontalHeaderLabels([f"Files to sync ({selected_row_index})"])

    def start_search_timer(self):
        self.search_timer.start(400)

    def filter_files(self):
        search_text = self.search_bar.text().lower()
        shown_unselected_files_count = 0
        shown_selected_files_count = 0
        for row in range(self.unselected_table.rowCount()):
            item = self.unselected_table.item(row, 0)
            if item and search_text not in item.text().lower():
                self.unselected_table.hideRow(row)
            else:
                self.unselected_table.showRow(row)
                shown_unselected_files_count += 1

        for row in range(self.selected_table.rowCount()):
            item = self.selected_table.item(row, 0)
            if item and search_text not in item.text().lower():
                self.selected_table.hideRow(row)
            else:
                self.selected_table.showRow(row)
                shown_selected_files_count += 1

        # Set table header to show number of files shown / all
        if shown_selected_files_count == self.selected_table.rowCount():
            self.selected_table.setHorizontalHeaderLabels(
                [f"Files to sync ({shown_selected_files_count})"]
            )
        else:
            self.selected_table.setHorizontalHeaderLabels(
                [f"Files to sync ({shown_selected_files_count}/{self.selected_table.rowCount()})"]
            )
        if shown_unselected_files_count == self.unselected_table.rowCount():
            self.unselected_table.setHorizontalHeaderLabels(
                [f"Files ({shown_unselected_files_count})"]
            )
        else:
            self.unselected_table.setHorizontalHeaderLabels(
                [f"Files ({shown_unselected_files_count}/{self.unselected_table.rowCount()})"]
            )

        QToolTip.hideText()

    def select_file(self, item):
        file_name = item.text()
        self.sync_files[file_name] = True
        self.populate_tables()

    def deselect_file(self, item):
        file_name = item.text()
        if file_name in self.sync_files:
            self.sync_files.pop(file_name)
        self.populate_tables()


def open_media_sync_dialog():
    parent = mw.app.activeWindow()
    config = Config()
    config.load()

    dialog = MediaSyncDialog(parent, config.sync_files)
    if dialog.exec():
        config.sync_files = dialog.sync_files
        config.save()
