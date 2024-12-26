import cv2
import numpy as np
import platform


import win32ui
import win32con
import win32gui


from src.utils.DataProcessor import get_title


class ScreenCapture(object):
    def __init__(self):
        self.os = platform.system()

    def __from_windows(self):
        self.__window_id = get_title()
        hwnd = win32gui.FindWindow(None, self.__window_id)
        if not hwnd:
            return np.array([])

        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top

        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bitmap)

        save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

        bmp_info = save_bitmap.GetInfo()
        bmp_str = save_bitmap.GetBitmapBits(True)

        image = np.frombuffer(bmp_str, dtype='uint8')
        image = image.reshape((bmp_info['bmHeight'], bmp_info['bmWidth'], 4))
        screenshot = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)

        # Clean up
        win32gui.DeleteObject(save_bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)

        screenshot = cv2.cvtColor(src=screenshot, code=cv2.COLOR_BGR2RGB)

        return cv2.resize(screenshot, (1024, 768))

    @property
    def updated_screenshot(self):
        return self.__from_windows()