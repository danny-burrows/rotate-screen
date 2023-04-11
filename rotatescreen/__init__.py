import platform

system = platform.system()
if system == "Windows":
    from .display_windows import *
elif system == "Linux":
    from .display_linux import *
else:
    raise Exception(f"ERROR: Platform '{system}' is not yet supported!")
