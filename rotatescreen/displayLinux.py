from Xlib import display
from Xlib.ext import randr

def __fetch_root_display_obj():
    return display.Display(":0")


def get_displays():
    d = __fetch_root_display_obj()

    


def get_primary_display():
    d = __fetch_root_display_obj()
    return d.screen(d.get_default_screen())


def __get_display_info():
    d = display.Display(":0")

    # Get primary screen...
    d.screen(d.get_default_screen())

    screen_count = d.screen_count()
    screen = 0
    info = d.screen(screen)
    window = info.root

def get_displays():
    d = display.Display(':0')
    screen_count = d.screen_count()
    default_screen = d.get_default_screen()
    result = []
    screen = 0
    info = d.screen(screen)
    window = info.root

    res = randr.get_screen_resources(window)
    for output in res.outputs:
        params = d.xrandr_get_output_info(output, res.config_timestamp)
        if not params.crtc:
           continue
        crtc = d.xrandr_get_crtc_info(params.crtc, res.config_timestamp)
        modes = set()
        for mode in params.modes:
            modes.add(find_mode(mode, res.modes))
        result.append({
            'name': params.name,
            'resolution': "{}x{}".format(crtc.width, crtc.height),
            'available_resolutions': list(modes)
        })

    return result





def get_secondary_displays():
    d = display.Display(':0')
    screen_count = d.screen_count()
    default_screen = d.get_default_screen()
    result = []
    screen = 0
    info = d.screen(screen)
    window = info.root

    res = randr.get_screen_resources(window)
    for output in res.outputs:
        params = d.xrandr_get_output_info(output, res.config_timestamp)
        if not params.crtc:
           continue
        crtc = d.xrandr_get_crtc_info(params.crtc, res.config_timestamp)
        modes = set()
        for mode in params.modes:
            modes.add(find_mode(mode, res.modes))
        result.append({
            'name': params.name,
            'resolution': "{}x{}".format(crtc.width, crtc.height),
            'available_resolutions': list(modes)
        })

    return result


class Display:

    def __init__(self, hMonitor):
        self.hMonitor = hMonitor

    def __repr__(self):
        return f"<'{self.device_description[0]}' object>"

    def rotate_to(self, degrees):
        if degrees == 90:
            rotation_val = win32con.DMDO_90
        elif degrees == 180:
            rotation_val = win32con.DMDO_180
        elif degrees == 270:
            rotation_val = win32con.DMDO_270
        elif degrees == 0:
            rotation_val = win32con.DMDO_DEFAULT
        else:
            raise ValueError("Display can only be rotated to 0, 90, 180, or 270 degrees.")

        dm = self.devicemodeW
        if((dm.DisplayOrientation + rotation_val) % 2 == 1):
            dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth
        dm.DisplayOrientation = rotation_val
        win32api.ChangeDisplaySettingsEx(self.device, dm)

    def set_landscape(self):
        self.rotate_to(0)

    def set_landscape_flipped(self):
        self.rotate_to(180)

    def set_portrait(self):
        self.rotate_to(90)

    def set_portrait_flipped(self):
        self.rotate_to(270)

    @property
    def current_orientation(self):
        state = self.devicemodeW.DisplayOrientation
        return state * 90

    @property
    def info(self):
        return win32api.GetMonitorInfo(self.hMonitor)

    @property
    def device(self):
        return self.info["Device"]

    @property
    def is_primary(self):
        # The only flag is MONITORINFOF_PRIMARY which is 1 only for the primary monitor.
        return self.info["Flags"]

    @property
    def device_description(self):
        display_device = win32api.EnumDisplayDevices(self.device)
        return display_device.DeviceString, display_device.DeviceID

    @property
    def devicemodeW(self):
        return win32api.EnumDisplaySettings(self.device, win32con.ENUM_CURRENT_SETTINGS)
