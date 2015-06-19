# pywmtouchhook
Simple hook class to get WM_TOUCH messages

This class is a simple hook to capture WM_TOUCH messages on Windows. It was tested on Windows 8 but should also work on Windows 7.

The WndProc iterception was inspired by:

http://wiki.wxpython.org/HookingTheWndProc

Unfortunately the ctypes method consistently crashed. The pywin32 method works, but the touch functions required were not available in pywin32. So, the class uses a combination of the two.

To use this class, simply start it, passing the HWND for which you wish to capture touch messages:

th = TouchHook(hwnd)

Fill out the handleTouchMessage method to do whatever you need to with touch events.
