import customtkinter as ctk
import ctypes
from list_manager import ListManager

def get_work_area():
    user32 = ctypes.windll.user32
    rect = ctypes.wintypes.RECT()
    SPI_GETWORKAREA = 48
    user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
    return rect.left, rect.top, rect.right, rect.bottom


class UI:
    def __init__(self):
        self.animating = False
        self.visible = False
        self.target_visible = False

        self.width = 250
        self.height = 600

        self.root = ctk.CTk()

        left, top, right, bottom = get_work_area()
        self.y = bottom - self.height

        self.x = -self.width
        self.root.geometry(f"{self.width}x{self.height}-{self.width}+{self.y}")
        self.root.overrideredirect(True)

        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.list_manager = ListManager()

        # 入力欄
        self.entry = ctk.CTkEntry(self.frame, placeholder_text="Add item...")
        self.entry.pack(fill="x", padx=10, pady=10)

        self.entry.bind("<Return>", self.add_item)

        # リスト表示フレーム
        self.list_frame = ctk.CTkScrollableFrame(self.frame)
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_list()

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
        end = 0

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

    # ----------------------
    # slide out
    # ----------------------

    def slide_out(self):
        self.target_visible = False

        if self.animating:
            return

        self.animating = True

        start = self.x
        end = -self.width

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
            widget.destroy()

        for item in self.list_manager.get_items():

            row = ctk.CTkFrame(self.list_frame)
            row.pack(fill="x", pady=2)
            row.grid_columnconfigure(0, weight=1)
            row.grid_columnconfigure(1, weight=0)

            label = ctk.CTkLabel(row, text=item, anchor="w")
            label.grid(row=0, column=0, sticky="ew", padx=5)

            delete_btn = ctk.CTkButton(
                row,
                text="✕",
                width=24,
                height=24,
                fg_color="transparent",
                hover_color="#ff5555",
                command=lambda i=item: self.delete_item(i)
            )
            delete_btn.grid(row=0, column=1, sticky="e", padx=5)

    def delete_item(self, text):
        self.list_manager.remove(text)
        self.refresh_list()