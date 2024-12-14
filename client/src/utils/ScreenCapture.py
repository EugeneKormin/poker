import cv2
import gi
import Xlib
import Xlib.display
from Xlib import X
import numpy as np


from src.utils.DataProcessor import get_title, get_title_by_window_name

gi.require_version('Gdk', '3.0')


class ScreenCapture(object):
    def __init__(self):
        title = get_title()
        self.__window_id = get_title_by_window_name(window_name=title)

    def __make(self):
        display = Xlib.display.Display()
        window = display.create_resource_object('window', self.__window_id)

        geometry = window.get_geometry()
        width, height = geometry.width, geometry.height

        pixmap = window.get_image(0, 0, width, height, X.ZPixmap, 0xffffffff)
        data = pixmap.data
        array = np.frombuffer(data, dtype='uint8').reshape((height, width, 4))
        screenshot = cv2.cvtColor(array, cv2.COLOR_RGBA2RGB)
        return cv2.resize(screenshot, (1024, 768))

    @property
    def updated_screenshot(self):
        screenshot = self.__make()
        return screenshot
