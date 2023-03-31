"""Implementation rotation for Mac-Os"""
import Quartz
import objc
import Foundation
import warnings
import platform

__all__ = ['Display', 'get_displays']

dict_of_funcs = {}


def init():
    global dict_of_funcs
    dict_of_funcs = {}
    RotationInit = objc.initFrameworkWrapper(  # Ignore warning.
     'IOKit',
     frameworkIdentifier='com.apple.iokit',
     frameworkPath=objc.pathForFramework('/System/Library/Frameworks/IOKit.framework'),
     globals=globals()  # Make function between IOKit and Pyton is global.
     )
    bridge_creator = Foundation.NSBundle.bundleWithIdentifier_('com.apple.framework.IOKit')
    function_list = [  # Create list with tuples include functions from IOKit bridge-support.
         ('IOServiceRequestProbe', b'iII'),  # Second argument is signature from tags <arg> in bridge support file.
         ('IODisplayCreateInfoDictionary', b'^{__CFDictionary=}II')
    ]

    objc.loadBundleFunctions(RotationInit, dict_of_funcs, function_list)
    objc.loadBundleFunctions(bridge_creator, globals(), function_list)


def get_displays():
    """Return all displays ID"""
    return Quartz.CGMainDisplayID()


class Display:

    def __init__(self):
        warnings.simplefilter("ignore")
        init()
        warnings.simplefilter('default')  # PyObjC warning when PyObjC 9.0.1 version using initFrameworkWrapper.
        self.rotation = Quartz.CGDisplayRotation(Quartz.CGMainDisplayID())

    @staticmethod
    def rotate_to(degrees):

        angle_num = {
             0: 0x00,

             90: 0x10 | 0x20 << 16,

             180: 0x20 | 0x40 << 16,  # Expanding 2 rotation values in 8-literal,
                                      # and create "long-long" type for objective-c.
             270: 0x10 | 0x40 << 16,

         }
        try:

            if degrees == 360:
                degrees = degrees.imag
            degrees += 360

            angle_ = angle_num[degrees]
            globals()['IOServiceRequestProbe'](Quartz.CGDisplayIOServicePort(Quartz.CGMainDisplayID()), 0x400 | angle_)

        except (KeyError, TypeError):
            raise ValueError(f'{degrees} Must be multiple to 90˚.')

    def rotation(self):
        return int(str(self.rotation))

    def set_landscape(self):
        self.rotate_to(0)

    def set_landscape_flipped(self):
        self.rotate_to(180)

    def set_portrait(self):
        self.rotate_to(90)

    def set_portrait_flipped(self):
        self.rotate_to(270)

    @staticmethod
    def info():
        return globals()['IODisplayCreateInfoDictionary'](Quartz.CGDisplayIOServicePort(Quartz.CGMainDisplayID()), 0)

    @staticmethod
    def device():
        return platform.platform(), platform.architecture(), platform.machine()
