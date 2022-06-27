import os

from libqtile import bar, qtile
from libqtile.config import Screen
from libqtile.lazy import lazy

from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration

from utils.settings import colors, two_monitors, wallpaper_main, wallpaper_sec, with_battery, workspace_names

import os

home = os.path.expanduser('~')


widget_defaults = dict(
    font="FiraCode Nerd Font",
    fontsize=15,
    padding=2,
    background=colors[12],
)
extension_defaults = widget_defaults.copy()

group_box_settings = {
    "active":                       colors[0],
    "block_highlight_text_color":   colors[0],
    "this_current_screen_border":   colors[0],
    "this_screen_border":           colors[0],
    "urgent_border":                colors[3],
    "background":                   colors[12],  # background is [10-12]
    "other_current_screen_border":  colors[12],
    "other_screen_border":          colors[12],
    "highlight_color":              colors[13],
    "inactive":                     colors[14],
    "foreground":                   colors[18],
    "borderwidth": 2,
    "disable_drag": True,
    "fontsize": 14,
    "highlight_method": "line",
    "padding_x": 10,
    "padding_y": 16,
    "rounded": False,
}

# Define functions for bar
# TODO

# Mouse_callback functions
def open_launcher():
    qtile.cmd_spawn("rofi -show drun -theme ~/.config/rofi/launcher.rasi")

def open_powermenu():
    qtile.cmd_spawn("" + home + "/.local/bin/power")

# TODO fix
def toggle_maximize():
    lazy.window.toggle_maximize()

def parse_window_name(text):
    """Simplifies the names of a few windows, to be displayed in the bar"""
    target_names = [
        'Mozilla Firefox',
        'Visual Studio Code',
        'Discord',
    ]
    return next(filter(lambda name: name in text, target_names), text)


base_decor = {
    "colour": colors[13],
    "filled": True,
    "padding_y": 4,
    "line_width": 0,
}


def create_bar():
    """Create top bar, defined as function to allow duplication in other monitors"""
    def _separator():
        return widget.Sep(
            # foreground=colors[18],
            foreground=colors[12],
            padding=4,
            linewidth=2,
            size_percent=55,
        )
    
    def _full_decor():
        return RectDecoration(
            radius=4,
            **base_decor,
        )
    
    def _left_decor():
        return RectDecoration(
            radius=[4, 0, 0, 4],
            **base_decor,
        )

    def _right_decor():
        return RectDecoration(
            radius=[0, 4, 4, 0],
            **base_decor,
        )

    
    battery_widget = (
        widget.Battery(
            format="{char} {percent:2.0%}",
            charge_char="",
            discharge_char="",
            full_char="",
            unknown_char="",
            empty_char="",
            show_short_text=False,
            foreground=colors[1],
            padding=8,
            decorations=[_full_decor()],
        ),
        _separator(),
    ) if with_battery else ()
    
    return bar.Bar(
        [
            widget.TextBox(
                # text=" ",
                # text="",
                text="ﮊ",
                font="FiraCode Nerd Font",
                fontsize=22,
                foreground='#000000',
                # foreground=colors[2],
                background=colors[0],
                padding=20,
                mouse_callbacks={"Button1": open_launcher},
            ),
            # Workspaces
            widget.GroupBox(  # WEB
                font="Font Awesome 6 Brands",
                visible_groups=[workspace_names[0]],
                **group_box_settings,
            ),
            widget.GroupBox(  # DEV, SYS
                font="Font Awesome 6 Free Solid",
                visible_groups=[workspace_names[1], workspace_names[2]],
                **group_box_settings,
            ),
            widget.GroupBox(  # DISC, MUS
                font="Font Awesome 6 Brands",
                visible_groups=[workspace_names[3], workspace_names[4]],
                **group_box_settings,
            ),
            widget.GroupBox(  # FILE, NOT
                font="Font Awesome 6 Free Solid",
                visible_groups=[workspace_names[5], workspace_names[6]],
                **group_box_settings,
            ),
            # Middle spacer
            widget.Spacer(),
            # Window name TODO
            widget.TextBox(
                text=" ",
                foreground='#ffffff',
                font="Font Awesome 6 Free Solid",
            ),
            widget.WindowName(
                foreground='#ffffff',
                width=bar.CALCULATED,
                empty_group_string="Desktop",
                max_chars=40,
                parse_text=parse_window_name,
                mouse_callbacks={"Button1": toggle_maximize},
            ),
            widget.Spacer(),
            # WM layout indicator
            widget.CurrentLayoutIcon(
                custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
                foreground=colors[2],
                padding=10,
                scale=0.5,
            ),
            _separator(),
            # Sound
            widget.TextBox(
                text="墳",
                foreground=colors[6],
                font="FiraCode Nerd Font",
                fontsize=20,
                padding=8,
                decorations=[_left_decor()],
            ),
            widget.PulseVolume(
                foreground=colors[6],
                limit_max_volume="True",
                # mouse_callbacks={"Button3": open_pavu},
                padding=8,
                decorations=[_right_decor()],
            ),
            _separator(),
            # Battery
            *battery_widget,
            # Clock
            widget.TextBox(
                text="",
                font="FiraCode Nerd Font",
                fontsize=16,
                foreground=colors[8],  # blue
                padding=8,
                decorations=[_left_decor()],
            ),
            widget.Clock(
                format="%b %d, %H:%M",
                foreground=colors[8],
                padding=8,
                decorations=[_right_decor()],
            ),
            _separator(),
            # Power button
            widget.TextBox(
                text="⏻",
                background=colors[0],
                foreground="#000000",
                font="Font Awesome 6 Free Solid",
                fontsize=18,
                padding=18,
                mouse_callbacks={"Button1": open_powermenu},
            ),
        ],
        30,
        margin=[4, 6, 2, 6],
        opacity=1,
    )

main_screen_bar = create_bar()
if two_monitors:
    secondary_screen_bar = create_bar()

screens = [
    Screen(
        wallpaper=wallpaper_main,
        wallpaper_mode="fill",
        top=main_screen_bar,
        bottom=bar.Gap(2),
        left=bar.Gap(2),
        right=bar.Gap(2),
    ),
]

if two_monitors:
    screens.append(
        Screen(
            wallpaper=wallpaper_sec,
            wallpaper_mode="fill",
            top=secondary_screen_bar,
            bottom=bar.Gap(2),
            left=bar.Gap(2),
            right=bar.Gap(2),
        ),
    )