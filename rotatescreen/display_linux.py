from Xlib import display
from Xlib.ext import randr
from typing import List, Tuple

# Create an X display and get the root window + its resources
d = display.Display()
root = d.screen().root
res = root.xrandr_get_screen_resources()


class Display:

    def __init__(self, output_id, crtc_id):
        self._output_id = output_id
        self._crtc_id = crtc_id

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

        # NOTE: seems to need to be done as calling self._crtc_info too many times results in https://github.com/python-xlib/python-xlib/issues/241
        crtc_info = self._crtc_info

        # Set screen size, if needed...
        if (self.current_orientation in (0, 180) and rotation_val in (randr.Rotate_90, randr.Rotate_270)) \
                or (self.current_orientation in (90, 270) and rotation_val in (randr.Rotate_0, randr.Rotate_180)):
            # Start with the flipped screen max's
            max_w = crtc_info.x + crtc_info.height
            max_h = crtc_info.y + crtc_info.width
            for display in get_displays():
                display_crtc_info = display._crtc_info
                max_w = max(max_w, display_crtc_info.x + display_crtc_info.width)
                max_h = max(max_h, display_crtc_info.y + display_crtc_info.height)

            screen_size_range = root.xrandr_get_screen_size_range()

            # NOTE: Chosen to allow xlib to omit parts of the screen that overflow max screen size instead of erroring.
            width = min(max(max_w, screen_size_range.min_width), screen_size_range.max_width)
            height = min(max(max_h, screen_size_range.min_height), screen_size_range.max_height)

            dpi = 96.0
            width_mm = int((25.4 * width) / dpi)
            height_mm = int((25.4 * height) / dpi)

            root.xrandr_set_screen_size(width=width, height=height,
                                        width_in_millimeters=width_mm, height_in_millimeters=height_mm)

        set_crtc_config_result = d.xrandr_set_crtc_config(
            crtc=self._crtc_id,
            rotation=rotation_val,
            x=crtc_info.x,
            y=crtc_info.y,
            mode=crtc_info.mode,
            outputs=crtc_info.outputs,
            config_timestamp=res.config_timestamp,
        )
        assert set_crtc_config_result.status == 0, f"xrandr failed to set crtc config for crtc id '{self._crtc_id}' on Display '{self}'"

    def set_landscape(self) -> None:
        self.rotate_to(0)

    def set_landscape_flipped(self) -> None:
        self.rotate_to(180)

    def set_portrait(self) -> None:
        self.rotate_to(90)

    def set_portrait_flipped(self) -> None:
        self.rotate_to(270)

    @property
    def _crtc_info(self):
        return d.xrandr_get_crtc_info(self._crtc_id, res.config_timestamp)

    @property
    def current_orientation(self) -> int:
        # Get the CRTC's current mode information
        mode_info = d.xrandr_get_crtc_info(self._crtc_id, res.config_timestamp)

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
        return self._output_id == primary_output

    @property
    def device_description(self) -> Tuple[str, str]:
        output_info = d.xrandr_get_output_info(self._output_id, res.config_timestamp)
        return output_info.name, str(self._crtc_id)

    # xlib-style aliases
    normal = set_landscape
    inverted = set_landscape
    left = set_portrait
    right = set_portrait_flipped


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
