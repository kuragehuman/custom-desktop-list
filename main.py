from ui import UI
from mouse_detector import MouseDetector

ui = UI()

mouse = MouseDetector(ui)
mouse.start()

ui.run()