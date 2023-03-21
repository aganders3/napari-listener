"""Create basic TCPServer that can recieve and execute app-model commands."""
import socketserver
import threading

import napari
from superqt import ensure_main_thread

from napari_listener import _actions

APP = napari._app_model.get_app()
APP.register_actions(_actions.ACTIONS)

ADDRESS, DEFAULT_PORT = "127.0.0.1", 40256


def new_server(start=True) -> socketserver.TCPServer:
    # look for an open port, start at DEFAULT_PORT and count up
    for port in range(DEFAULT_PORT, DEFAULT_PORT + 100):
        try:
            server = socketserver.TCPServer(
                (ADDRESS, port),
                AppModelCommandRequestHandler,
            )
        except OSError:
            pass
        else:
            break
    else:
        raise RuntimeError("unable to find available port")

    if start:
        threading.Thread(
            target=server.serve_forever,
            daemon=True,
        ).start()
    return server


class AppModelCommandRequestHandler(socketserver.BaseRequestHandler):
    history = None

    def handle(self):
        data = self.request.recv(2048).strip().decode()
        # TODO: do some smarter parsing here
        command, *args = data.split(" ")
        ensure_main_thread(self.exec_app_model_command)(command, args)

    def exec_app_model_command(self, command, args):
        if self.history is not None:
            self.history.append(f"command: {command}")
            self.history.append(f"args: {args}")
            self.history.append("-" * 8)
        APP.commands.execute_command(command, *args).result()
