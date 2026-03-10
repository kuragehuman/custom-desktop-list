import json
import os

def get_config_path():

    appdata = os.getenv("APPDATA")

    if not appdata:
        appdata = os.path.expanduser("~")

    base = os.path.join(appdata, "custom-desktop-list")

    os.makedirs(base, exist_ok=True)

    return os.path.join(base, "config.json")



class ListManager:

    def __init__(self, app):
        self.app = app
        appdata = os.getenv("APPDATA")
        self.folder = os.path.join(appdata, "custom-desktop-list")
        self.file = os.path.join(self.folder, "list.json")

        os.makedirs(self.folder, exist_ok=True)

        if not os.path.exists(self.file):
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump([], f)

        self.items = self.load()

    def load(self):
        with open(self.file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.items, f, indent=2, ensure_ascii=False)

    def add(self, text):
        text = text.strip()

        if not text:
            return

        self.items.append(text)
        self.save()

    def get_items(self):
        return self.items
    
    def remove(self, text):
        if text in self.items:
            self.items.remove(text)
            self.save()
    def move(self, item, target):

        items = self.items

        if item not in items or target not in items:
            return

        items.remove(item)

        index = items.index(target)

        items.insert(index, item)

        self.save()
    def move_index(self, from_i, to_i):

        item = self.items.pop(from_i)

        self.items.insert(to_i, item)

        self.save()
    
    def reset(self):

        config_path = get_config_path()

        try:

            if os.path.exists(self.file):
                os.remove(self.file)

            if os.path.exists(config_path):
                os.remove(config_path)

            self.items = []

        except Exception as e:
            print("reset error:", e)
    
    def load_config(self):

        path = get_config_path()

        if os.path.exists(path):

            with open(path, "r") as f:
                data = json.load(f)

                self.app.position = data.get("position", self.app.position)


    def save_config(self):

        path = get_config_path()

        data = {
            "position": self.app.position
        }

        with open(path, "w") as f:
            json.dump(data, f)
