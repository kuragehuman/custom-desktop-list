from pynput import mouse
import threading


class MouseDetector:

    def __init__(self, ui):
        self.ui = ui

    def start(self):
        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):

        def on_move(x, y):

            left = self.ui.visible_x
            right = self.ui.visible_x + self.ui.width
            top = self.ui.y
            bottom = self.ui.y + self.ui.height

            # LEFT SIDE
            if self.ui.side == "left":

                if x <= left + 5 and top <= y <= bottom:
                    self.ui.slide_in()

                elif x > left + self.ui.width + 20:
                    self.ui.slide_out()

            # RIGHT SIDE
            else:

                if x >= right - 5 and top <= y <= bottom:
                    self.ui.slide_in()

                elif x < right - self.ui.width - 20:
                    self.ui.slide_out()

        with mouse.Listener(on_move=on_move) as listener:
            listener.join()