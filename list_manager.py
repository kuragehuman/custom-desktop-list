import json
import os


class ListManager:

    def __init__(self):
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