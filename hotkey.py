# from pynput import keyboard
# import threading


# class HotkeyListener:

#     def __init__(self, ui):
#         self.ui = ui

#     def start(self):
#         threading.Thread(target=self.listen, daemon=True).start()

#     def listen(self):

#         COMBO = {
#             keyboard.Key.ctrl_l,
#             keyboard.Key.shift,
#             keyboard.Key.space
#         }

#         current = set()

#         def on_press(key):

#             if key in COMBO:
#                 current.add(key)

#             if all(k in current for k in COMBO):

#                 # UIスレッドで実行
#                 def toggle():

#                     if not self.ui.visible:
#                         self.ui.show()
#                     else:
#                         self.ui.hide()

#                 self.ui.root.after(0, toggle)

#         def on_release(key):

#             if key in current:
#                 current.remove(key)

#         with keyboard.Listener(
#             on_press=on_press,
#             on_release=on_release
#         ) as listener:

#             listener.join()