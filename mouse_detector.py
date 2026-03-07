import pyautogui
import threading
import time

class MouseDetector:
    def __init__(self, ui):
        self.ui = ui

    def start(self):
        threading.Thread(target=self.loop, daemon=True).start()

    def loop(self):
        while True:
            x, y = pyautogui.position()

            if x <= 5:
                self.ui.slide_in()

            elif x > self.ui.width:
                self.ui.slide_out()

            time.sleep(0.05)