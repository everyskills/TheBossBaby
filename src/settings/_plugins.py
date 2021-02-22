import os

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class PluginPage:
    def __init__(self, parent) -> None:
        super().__init__()
