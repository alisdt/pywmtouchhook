import win32gui
import win32con

import ctypes
RegisterTouchWindow = ctypes.windll.user32.RegisterTouchWindow
GetTouchInputInfo = ctypes.windll.user32.GetTouchInputInfo
from ctypes import c_long, c_uint32, c_void_p
from ctypes import pointer, sizeof

import sys

LONG, HANDLE, DWORD, ULONG_PTR = c_long, c_void_p, c_uint32, c_void_p

class TOUCHINPUT(ctypes.Structure):
    _fields_ = [
        ("x", LONG),
        ("y", LONG),
        ("hSource", HANDLE),
        ("dwID", DWORD),
        ("dwFlags", DWORD),
        ("dwMask", DWORD),
        ("dwTime", DWORD),
        ("dwExtraInfo", ULONG_PTR),
        ("cxContact", DWORD),
        ("cyContact", DWORD)
    ]

    def __repr__(self):
        return " ".join([str(getattr(self, f)) for f, _ in self._fields_])+"\n"

class TouchHook(object):
    def __init__(self, hwnd):
        # Set the WndProc to our function
        self.oldWndProc = win32gui.SetWindowLong(hwnd, win32con.GWL_WNDPROC, self.wndProc)

        # TWF_FINETOUCH and TWF_WANTPALM: see
        # https://msdn.microsoft.com/en-us/library/windows/desktop/dd317326%28v=vs.85%29.aspx
        rtn = RegisterTouchWindow(hwnd, 0x00000001 | 0x00000002)
        assert rtn, "Couldn't register for touch messages"

    def handleTouchMessage(self, cTouches, hInfo):
        TOUCHINPUTARRAY = TOUCHINPUT*cTouches
        touches_array = TOUCHINPUTARRAY()
        rtn = GetTouchInputInfo(hInfo, cTouches, pointer(touches_array), sizeof(TOUCHINPUT))
        if rtn:
            print touches_array
        else:
            sys.stderr.write("{:X}\n".format(ctypes.GetLastError()))

    def wndProc(self, hwnd, msg, wparam, lparam):
        if msg == 0x240:
            self.handleTouchMessage(wparam, lparam)
            return 0 # handled
        return win32gui.CallWindowProc(self.oldWndProc, hwnd, msg, wparam, lparam)
