import socket

import pytest
from app_model.types import Action
from qtpy.QtWidgets import QPushButton

from napari_listener import SocketWidget
from napari_listener._app_model_handler import ADDRESS, APP, DEFAULT_PORT


@pytest.fixture
def socket_widget():
    widget = SocketWidget()
    yield widget
    widget._stop_listening()


@pytest.fixture
def dummy_action(qtbot):
    button = QPushButton()
    qtbot.add_widget(button)
    action = Action(
        id="napari:napari_listener:test",
        title="Action Test Fixture",
        callback=lambda: button.click(),
    )
    unregister_fn = APP.register_action(action)
    yield action, button
    unregister_fn()


def test_create_socket_widget(socket_widget, qtbot):
    assert socket_widget.server is not None
    assert socket_widget.server.server_address[0] == ADDRESS
    assert socket_widget.server.server_address[1] in range(
        DEFAULT_PORT, DEFAULT_PORT + 100
    )


def test_server_already_running(socket_widget, qtbot):
    server = socket_widget.server
    socket_widget._start_listening()
    assert socket_widget.server is server


def test_default_port_occupied(socket_widget, qtbot):
    server = socket_widget.server.server_address
    socket_widget._stop_listening()
    s = socket.create_server(server)
    s.listen()
    socket_widget._start_listening()
    assert socket_widget.server.server_address[0] == ADDRESS
    assert socket_widget.server.server_address[1] != server[1]
    s.close()


def test_stop_start_listener(socket_widget, qtbot):
    socket_widget.stop_button.click()
    assert socket_widget.server is None

    socket_widget.start_button.click()
    assert socket_widget.server is not None


def test_app_model_command(dummy_action, socket_widget, qtbot):
    server = socket_widget.server.server_address
    action, button = dummy_action
    data = action.id + "\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(server)
        with qtbot.waitSignal(button.clicked, timeout=10_000):
            sock.sendall(data.encode())
