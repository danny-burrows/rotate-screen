import win32api
import win32con


def get_displays():
    displays = [Display(hMonitor) for hMonitor,_,_ in win32api.EnumDisplayMonitors()]
    return displays


def get_primary_display():
    for display in get_displays():
        if display.is_primary:
            return display


def get_secondary_displays():
    displays = [display for display in get_displays() if not display.is_primary]
    return displays


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
