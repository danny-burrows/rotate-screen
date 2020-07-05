import rotatescreen
import keyboard

screen = rotatescreen.get_primary_display()

keyboard.add_hotkey('ctrl+alt+up', screen.set_landscape, suppress=True)
keyboard.add_hotkey('ctrl+alt+right', screen.set_portrait_flipped, suppress=True)
keyboard.add_hotkey('ctrl+alt+down', screen.set_landscape_flipped, suppress=True)
keyboard.add_hotkey('ctrl+alt+left', screen.set_portrait, suppress=True)

keyboard.wait()
