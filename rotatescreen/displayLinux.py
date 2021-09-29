from __future__ import print_function

print("Linux Detected!")

from Xlib import X, display
from Xlib.ext import randr
from Xlib.error import DisplayNameError

try:
    d = display.Display()
except DisplayNameError:
    print("Error getting display.")
    exit()

s = d.screen()
window = s.root.create_window(0, 0, 1, 1, 1, s.root_depth)

res = randr.get_screen_resources(window)
for mode in res.modes:
    w, h = mode.width, mode.height
    print("Width: {}, height: {}".format(w, h))