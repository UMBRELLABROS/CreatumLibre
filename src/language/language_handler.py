import json
import os

class LanguageHandler:
    def __init__(self, lang="en"):
        self.lang = lang
        self.translations = self.load_translations()

    def load_translations(self):
        path = os.path.join(os.path.dirname(__file__), "translations.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_text(self, key):
        return self.translations.get(key, {}).get(self.lang, self.translations.get(key, {}).get("en", key))