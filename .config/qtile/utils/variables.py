import json
from utils import dir

directory = f'{dir.get()}/settings.json'

variables = {
    'bar': 'decorated',
    'colorscheme': 'catppuccin',
    'terminal': 'kitty',
    'wallpaper_main': '~/.config/qtile/wallpapers/mini_black_hole.png',
    'wallpaper_sec': '~/.config/qtile/wallpapers/mini_black_hole.png',
    'with_battery': False,
    'with_wlan': False,
    'two_monitors': False,
}


def load_settings(cls):
    def wrap():
        instance = cls()
        instance.settings = read_settings_file()
        return instance

    def read_settings_file():
        try:
            with open(directory) as f:
                return dict(json.load(f)[0])
        except (json.JSONDecodeError, FileNotFoundError):
            return default_settings[0]

    return wrap


@load_settings
class Variables:
    def __init__(self):
        pass

    def __getattr__(self, name):
        value = self.settings.get(name)
        if isinstance(value, dict):
            sub_instance = Variables()
            sub_instance.settings = value
            return sub_instance

    def __getitem__(self, name):
        return self.settings[name]
    
    def get(self, key, default=None):
        return self.settings.get(key, default)


var = Variables()
