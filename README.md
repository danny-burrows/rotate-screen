# Rotate Screen
A small Python package for rotating the screen.

## Platforms Supported
Windows is currently the only platform supported.

## Installation
Clone the repo or download as zip then navigate to the project root directory and use the following command...
```sh
pip install rotate-screen
```

## Example: ![Ctrl+Alt+Arrow Shortcut](https://github.com/TheBrokenEstate/rotate-screen/blob/master/examples/shortcuts.py)
This is a simple example that implements the 'Ctrl+Alt+Arrow' shortcut for rotating the display. Some graphics cards don't come with this capability by default.

This example requires the keyboard module...
```sh
pip install keyboard
```
Here is the code! This module adds hotkeys to rotate the main display to the corresponding arrow keys.
```python
import rotatescreen
import keyboard

screen = rotatescreen.get_primary_display()

keyboard.add_hotkey('ctrl+alt+up', screen.set_landscape, suppress=True)
keyboard.add_hotkey('ctrl+alt+right', screen.set_portrait_flipped, suppress=True)
keyboard.add_hotkey('ctrl+alt+down', screen.set_landscape_flipped, suppress=True)
keyboard.add_hotkey('ctrl+alt+left', screen.set_portrait, suppress=True)

keyboard.wait()
```

## Example: ![Do A Barrel Roll](https://github.com/TheBrokenEstate/rotate-screen/blob/master/examples/do-a-barrel-roll.py)
This was a little joke script to show off some more of the modules functionality, due to the way windows rotates the display this is a pretty horrific looking, but entertaining. :)
```python
import rotatescreen
import time

screen = rotatescreen.get_primary_display()
start_pos = screen.current_orientation

for i in range(1, 5):
    pos = abs((start_pos - i*90) % 360)
    screen.rotate_to(pos)
    time.sleep(1.5)
```
