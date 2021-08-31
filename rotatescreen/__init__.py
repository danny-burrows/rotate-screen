try:
    from .displayWindows import *
except ImportError:
    from .displayLinux import *
