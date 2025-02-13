import json
from utils import dir
from typing import Any, Callable, TypeVar


T = TypeVar("T", bound="Variables")

directory: str = f"{dir.get()}/settings.json"

default_settings: list[dict[str, Any]] = [
    {
        "general": {
            "mod": "mod1",
            "network": "ens33",
            "two_monitors": True,
            "with_battery": False,
            "with_wlan": False,
        },
        "applications": {
            "terminal": "kitty",
            "editor": "vscodium",
            "browser": "librewolf",
            "app_launcher": "rofi -show drun",
            "mail_client": "thunderbird",
            "note_app": "obsidian",
            "screenshot_app": "flameshot gui",
        },
        "theme": {
            "bar": "decorated",
            "colorscheme": "catppuccin.json",
            "wallpapers": {
                "wallpaper_main": "~/pictures/wallpapers/floating_astronaut.png",
                "wallpaper_sec": "~/pictures/wallpapers/floating_astronaut.png",
            },
            "workspace_names": {
                "workspace_0": "\ue007",
                "workspace_1": "\uf121",
                "workspace_2": "\uf120",
                "workspace_3": "\uf70e",
                "workspace_4": "\uf0e0",
                "workspace_5": "\uf167",
                "workspace_6": "\uf1bc",
                "workspace_7": "\uf412",
                "workspace_8": "\uf4f9",
            },
        },
    }
]


def load_settings(cls: type[T]) -> Callable[[], T]:
    def wrap() -> T:
        instance: T = cls()
        instance.settings = read_settings_file()
        return instance

    def read_settings_file() -> dict[str, Any]:
        try:
            with open(directory) as f:
                return dict(json.load(f)[0])
        except (json.JSONDecodeError, FileNotFoundError):
            return default_settings[0]

    return wrap


@load_settings
class Variables:
    def __init__(self):
        self.settings: dict[str, Any]

    def __getattr__(self, name):
        value = self.settings.get(name)
        if isinstance(value, dict):
            sub_instance = Variables()
            sub_instance.settings = value
            return sub_instance

    def __getitem__(self, name):
        return self.settings[name]
    
    def __repr__(self):
        return str(self.settings)

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def get_workspace_names_list(self) -> list[str]:
        workspace_names = self.theme.get("workspace_names").values()
        return list(workspace_names)


var = Variables()
