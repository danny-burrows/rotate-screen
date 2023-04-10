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

        # NOTE: seems to need to be done as calling self.crtc_info too many times results in https://github.com/python-xlib/python-xlib/issues/241
        crtc_info = self.crtc_info

        # Set screen size, if needed...
        if (self.current_orientation in (0, 180) and rotation_val in (randr.Rotate_90, randr.Rotate_270)) \
                or (self.current_orientation in (90, 270) and rotation_val in (randr.Rotate_0, randr.Rotate_180)):
            # Start with the flipped screen max's
            max_w = crtc_info.x + crtc_info.height
            max_h = crtc_info.y + crtc_info.width
            for display in get_displays():
                display_crtc_info = display.crtc_info
                max_w = display_crtc_info.x + display_crtc_info.width if display_crtc_info.x + display_crtc_info.width > max_w else max_w
                max_h = display_crtc_info.y + display_crtc_info.height if display_crtc_info.y + display_crtc_info.height > max_h else max_h

            # TODO: Need to calculate width_in_millimeters and height_in_millimeters! Perhaps can be done using DPI...
            root.xrandr_set_screen_size(width=max_w, height=max_h,
                                        width_in_millimeters=max_w, height_in_millimeters=max_h)

        d.xrandr_set_crtc_config(
            crtc=self.crtc_id,
            rotation=rotation_val,
            x=crtc_info.x,
            y=crtc_info.y,
            mode=crtc_info.mode,
            outputs=crtc_info.outputs,
            config_timestamp=res.config_timestamp,
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
    def crtc_info(self):
        return d.xrandr_get_crtc_info(self.crtc_id, res.config_timestamp)

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
