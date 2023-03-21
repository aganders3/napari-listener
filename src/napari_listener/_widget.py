import napari
from qtpy.QtWidgets import QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget

from napari_listener._app_model_handler import (
    AppModelCommandRequestHandler,
    new_server,
)

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"


class SocketWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.app = napari._app_model.get_app()
        self.server = None

        layout = QVBoxLayout()
        self.socket_label = QLabel("Not listening", parent=self)
        layout.addWidget(self.socket_label)

        self.start_button = QPushButton("Start", parent=self)
        self.start_button.clicked.connect(self._start_listening)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop", parent=self)
        self.stop_button.clicked.connect(self._stop_listening)
        layout.addWidget(self.stop_button)

        self.history = QTextEdit(readOnly=True)
        layout.addWidget(self.history)

        self.setLayout(layout)
        self.update_button()

        AppModelCommandRequestHandler.history = self.history

        # automatically start when launched
        self._start_listening()

    def _start_listening(self):
        if self.server is not None:
            # already started
            return
        else:
            self.server = new_server()

        self.update_button()

    def _stop_listening(self):
        if self.server is not None:
            self.server.shutdown()
            self.server = None
            self.update_button()

    def update_button(self):
        if self.server is not None:
            address = self.server.server_address
            self.socket_label.setText(f"Listening on {address[0]}:{address[1]}")
            self.start_button.hide()
            self.stop_button.show()
        else:
            self.socket_label.setText("Not listening")
            self.start_button.show()
            self.stop_button.hide()
