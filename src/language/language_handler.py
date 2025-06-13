import json
from pathlib import Path


class LanguageHandler:
    """Handles language translations for the application."""

    def __init__(self, lang="en"):
        self.lang = lang
        self.translations = self.load_translations()

    def get_lanaguage(self):
        return self.lang

    def load_translations(self):
        path = Path(__file__).parent / "translations.json"
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def get_text(self, key):
        return self.translations.get(key, {}).get(
            self.lang, self.translations.get(key, {}).get("en", key)
        )

    def set_language(self, lang):
        if lang in self.translations:
            self.lang = lang
        else:
            raise ValueError(f"Language '{lang}' not supported.")


lang_handler = LanguageHandler("de")
