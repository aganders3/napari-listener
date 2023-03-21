"""Custom demo actions to show off napari control via socket."""
from app_model.types import Action
from napari.viewer import Viewer


def open_file(filename: str, *, viewer: Viewer):
    viewer._window.activate()
    viewer.open(filename, stack=True)


ACTIONS = [
    Action(
        id="napari:open-file",
        title="Open File",
        callback=open_file,
    ),
]
