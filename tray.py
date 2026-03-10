import pystray
from PIL import Image, ImageDraw
import threading


def create_image():

    size = 64
    image = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(image)

    # 外枠
    margin = 6
    draw.rectangle(
        (margin, margin, size - margin, size - margin),
        outline="black",
        width=3
    )

    # 行の位置
    rows = [20, 32, 44]

    for y in rows:

        # テキスト線
        draw.line(
            (14, y, 38, y),
            fill="black",
            width=3
        )

        # 赤い削除ボタン
        draw.ellipse(
            (42, y - 4, 50, y + 4),
            fill="red"
        )

    return image


class TrayIcon:

    def __init__(self, app):
        self.app = app

        self.icon = pystray.Icon(
            "desktop_list",
            create_image(),
            "Desktop List",
            menu=self.create_menu()
        )

    # ----------------------

    def create_menu(self):

        return pystray.Menu(

            pystray.MenuItem("表示", self.show_window),

            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "左上",
                self.top_left,
                checked=lambda item: self.app.position == "top_left"
            ),
            pystray.MenuItem(
                "左下",
                self.bottom_left,
                checked=lambda item: self.app.position == "bottom_left"
            ),
            pystray.MenuItem(
                "右上",
                self.top_right,
                checked=lambda item: self.app.position == "top_right"
            ),
            pystray.MenuItem(
                "右下",
                self.bottom_right,
                checked=lambda item: self.app.position == "bottom_right"
            ),

            pystray.Menu.SEPARATOR,
            pystray.MenuItem('リスト・設定の削除', self.app.clear_list),

            pystray.MenuItem("終了", self.quit_app)
        )

    # ----------------------

    def run(self):
        threading.Thread(target=self.icon.run, daemon=True).start()

    # ----------------------
    # window
    # ----------------------

    def show_window(self, icon, item):
        self.app.root.after(0, self.app.show)

    # ----------------------
    # position
    # ----------------------

    def top_left(self, icon, item):
        self.app.root.after(0, lambda: self.app.set_position("top_left"))

    def top_right(self, icon, item):
        self.app.root.after(0, lambda: self.app.set_position("top_right"))

    def bottom_left(self, icon, item):
        self.app.root.after(0, lambda: self.app.set_position("bottom_left"))

    def bottom_right(self, icon, item):
        self.app.root.after(0, lambda: self.app.set_position("bottom_right"))

    # ----------------------

    def quit_app(self, icon, item):
        self.icon.stop()
        self.app.root.after(0, self.app.root.quit)