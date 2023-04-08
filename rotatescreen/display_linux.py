from Xlib import display
from Xlib.ext import randr
from typing import Dict, List, Tuple

# TODO: Is having these at the global level ok?
d = display.Display()
# Create an X display and get the root window
root = d.screen().root
# Get the resources for the root window
res = root.xrandr_get_screen_resources()


class Display:

    def __init__(self, output_id, crtc_id):
        self.output_id = output_id
        self.crtc_id = crtc_id

    def __repr__(self):
        return f"<'{self.device_description[0]}' object>"

    def rotate_to(self, degrees: int) -> None:
        if degrees == 90:
            rotation_val = randr.Rotate_90
        elif degrees == 180:
            rotation_val = randr.Rotate_180
        elif degrees == 270:
            rotation_val = randr.Rotate_270
        elif degrees == 0:
            rotation_val = randr.Rotate_0
        else:
            raise ValueError("Display can only be rotated to 0, 90, 180, or 270 degrees.")

        # Get this CRTC's current mode and position
        crtc = d.xrandr_get_crtc_info(self.crtc_id, res.config_timestamp)
        x, y, mode = crtc.x, crtc.y, crtc.mode

        d.xrandr_set_crtc_config(
            crtc=self.crtc_id,
            config_timestamp=res.config_timestamp,
            x=x,
            y=y,
            mode=mode,
            rotation=rotation_val,
            outputs=crtc.outputs
        )

    def set_landscape(self) -> None:
        self.rotate_to(0)

    def set_landscape_flipped(self) -> None:
        self.rotate_to(180)

    def set_portrait(self) -> None:
        self.rotate_to(90)

    def set_portrait_flipped(self) -> None:
        self.rotate_to(270)

    @property
    def current_orientation(self) -> int:
        # Get the CRTC's current mode information
        mode_info = d.xrandr_get_crtc_info(self.crtc_id, res.config_timestamp)

        # Get the CRTC's current rotation
        rotation = mode_info.rotation
        if rotation == randr.Rotate_0:
            return 0
        elif rotation == randr.Rotate_90:
            return 90
        elif rotation == randr.Rotate_180:
            return 180
        elif rotation == randr.Rotate_270:
            return 270

    @property
    def is_primary(self) -> bool:
        primary_output = root.xrandr_get_output_primary().output
        return self.output_id == primary_output

    @property
    def device_description(self) -> Tuple[str, str]:
        output_info = d.xrandr_get_output_info(self.output_id, res.config_timestamp)
        return output_info.name, self.crtc_id


def get_displays() -> List[Display]:
    displays = []
    for output_id in res.outputs:
        output_info = d.xrandr_get_output_info(output_id, res.config_timestamp)
        if output_info.crtc:
            displays.append(Display(output_id, output_info.crtc))
    return displays


def get_primary_display() -> Display | None:
    for display in get_displays():
        if display.is_primary:
            return display


def get_secondary_displays() -> List[Display]:
    displays = [display for display in get_displays() if not display.is_primary]
    return displays
