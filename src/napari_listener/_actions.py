"""Custom demo actions to show off napari control via socket."""
from app_model.types import Action
from napari._qt.qt_main_window import Window
from napari.viewer import Viewer


def open_file(filename: str, *, viewer: Viewer):
    viewer._window.activate()
    viewer.open(filename, stack=True)


def open_plugin_manager(window: Window):
    window.activate()
    window.plugins_menu._show_plugin_install_dialog()


ACTIONS = [
    Action(
        id="napari:open-file",
        title="Open File",
        callback=open_file,
    ),
    Action(
        id="napari:plugin-manager",
        title="Open Plugin Manager",
        callback=open_plugin_manager,
    ),
]
