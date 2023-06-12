import platform

system = platform.system()
if system == "Windows":
    from .display import *
elif system == "Darwin":
    from .mac_display import *
else:
    raise Exception(f"ERROR: Platform '{system}' is not yet supported!")