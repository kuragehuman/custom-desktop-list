import customtkinter as ctk
import ctypes
from ctypes import wintypes
from list_manager import ListManager
from tray import TrayIcon
import json
import os
# from hotkey import HotkeyListener

def get_corner_workarea(corner):

    user32 = ctypes.windll.user32

    SM_XVIRTUALSCREEN = 76
    SM_YVIRTUALSCREEN = 77
    SM_CXVIRTUALSCREEN = 78
    SM_CYVIRTUALSCREEN = 79

    vx = user32.GetSystemMetrics(SM_XVIRTUALSCREEN)
    vy = user32.GetSystemMetrics(SM_YVIRTUALSCREEN)
    vw = user32.GetSystemMetrics(SM_CXVIRTUALSCREEN)
    vh = user32.GetSystemMetrics(SM_CYVIRTUALSCREEN)

    left = vx
    top = vy
    right = vx + vw
    bottom = vy + vh

    if corner == "top_left":
        x, y = left + 1, top + 1
    elif corner == "top_right":
        x, y = right - 1, top + 1
    elif corner == "bottom_left":
        x, y = left + 1, bottom - 1
    else:
        x, y = right - 1, bottom - 1

    pt = wintypes.POINT(x, y)

    MONITOR_DEFAULTTONEAREST = 2
    hMonitor = user32.MonitorFromPoint(pt, MONITOR_DEFAULTTONEAREST)

    class MONITORINFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.DWORD),
            ("rcMonitor", wintypes.RECT),
            ("rcWork", wintypes.RECT),
            ("dwFlags", wintypes.DWORD)
        ]

    mi = MONITORINFO()
    mi.cbSize = ctypes.sizeof(mi)

    user32.GetMonitorInfoW(hMonitor, ctypes.byref(mi))

    r = mi.rcWork

    return r.left, r.top, r.right, r.bottom

def get_work_area():
    user32 = ctypes.windll.user32
    rect = ctypes.wintypes.RECT()
    SPI_GETWORKAREA = 48
    user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
    return rect.left, rect.top, rect.right, rect.bottom


class UI:
    def __init__(self):

        # drag state
        self.drag_row = None
        self.drag_start_y = 0

        # position
        self.side = "left"
        self.position = "bottom_left"

        # animation
        self.animating = False
        self.visible = False
        self.target_visible = False

        self.width = 250
        self.height = 600

        self.root = ctk.CTk()
        self.root.overrideredirect(True)

        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.list_manager = ListManager(self)

        self.list_manager.load_config()

        # input
        self.entry = ctk.CTkEntry(self.frame, placeholder_text="Add item...")
        self.entry.pack(fill="x", padx=10, pady=10)
        self.entry.bind("<Return>", self.add_item)

        # list
        self.list_frame = ctk.CTkScrollableFrame(self.frame)
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_list()

        # tray
        self.tray = TrayIcon(self)
        self.tray.run()

        # hotkey
        # self.hotkey = HotkeyListener(self)
        # self.hotkey.start()

        self.update_position()

    # ----------------------
    # position function
    # ----------------------
    def update_position(self):

        left, top, right, bottom = get_corner_workarea(self.position)

        if "left" in self.position:

            self.side = "left"
            self.visible_x = left
            self.hidden_x = left - self.width

        else:

            self.side = "right"
            self.visible_x = right - self.width
            self.hidden_x = right

        if "top" in self.position:
            self.y = top
        else:
            self.y = bottom - self.height

        self.x = self.hidden_x

        self.root.geometry(
            f"{self.width}x{self.height}+{self.x}+{self.y}"
        )

    def set_position(self, pos):
        self.position = pos
        self.update_position()
        self.list_manager.save_config()
        
    # ----------------------
    # easing functions
    # ----------------------

    def ease_out(self, t):
        return 1 - (1 - t) ** 3

    def ease_in(self, t):
        return t ** 3

    # ----------------------
    # slide in
    # ----------------------

    def slide_in(self):

        self.root.attributes("-topmost", True)
        self.root.lift()

        self.target_visible = True

        if self.animating:
            return

        self.animating = True

        start = self.x
        end = self.visible_x

        duration = 0.25
        steps = 30
        delay = int(duration / steps * 1000)

        def animate(step=0):
            if not self.target_visible:
                self.animating = False
                self.slide_out()
                return

            if step > steps:
                self.x = end
                self.visible = True
                self.animating = False
                return

            t = step / steps
            eased = self.ease_out(t)

            self.x = int(start + (end - start) * eased)

            self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
            self.root.after(delay, animate, step + 1)

        animate()
        
        self.entry.focus_set()      # 入力欄にフォーカス

    # ----------------------
    # slide out
    # ----------------------

    def slide_out(self):

        self.target_visible = False

        if self.animating:
            return

        self.animating = True

        start = self.x
        end = self.hidden_x

        duration = 0.25
        steps = 30
        delay = int(duration / steps * 1000)

        def animate(step=0):
            if self.target_visible:
                self.animating = False
                self.slide_in()
                return

            if step > steps:
                self.x = end
                self.visible = False
                self.animating = False
                return

            t = step / steps
            eased = self.ease_in(t)

            self.x = int(start + (end - start) * eased)

            self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
            self.root.after(delay, animate, step + 1)

        animate()

    # ----------------------

    def show(self):
        if not self.visible or self.animating:
            self.slide_in()

    def hide(self):
        if self.visible or self.animating:
            self.slide_out()

    def run(self):
        self.root.mainloop()
        
    def add_item(self, event=None):
        text = self.entry.get()

        self.list_manager.add(text)

        self.entry.delete(0, "end")

        self.refresh_list()


    def refresh_list(self):

        for widget in self.list_frame.winfo_children():
            widget.after(0, widget.destroy)

        for item in self.list_manager.get_items():

            row = ctk.CTkFrame(self.list_frame)
            row.item = item
            row.pack(fill="x", pady=2)

            label = ctk.CTkLabel(row, text=item, anchor="w")
            label.pack(side="left", fill="x", expand=True, padx=5)

            delete_btn = ctk.CTkButton(
                row,
                text="✕",
                width=24,
                height=24,
                fg_color="transparent",
                hover_color="#ff5555",
                command=lambda i=item: self.delete_item(i)
            )
            delete_btn.pack(side="right")
            
    def delete_item(self, text):
        self.list_manager.remove(text)
        self.refresh_list()

    def clear_list(self):
        self.list_manager.reset()
        self.refresh_list()
        self.position = "bottom_left"
        self.update_position()