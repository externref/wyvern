from __future__ import annotations


import attrs

LOCALE_TUPLES: list[tuple[str, str, str]] = [
    ("da", "Danish", "Dansk"),
    ("de", "German", "Deutsch"),
    ("en-GB", "English UK", "English UK"),
    ("en-US", "English US", "English US"),
    ("es-ES", "Spanish", "Español"),
    ("fr", "French", "Français"),
    ("hr", "Croatian", "Hrvatski"),
    ("it", "Italian", "Italiano"),
    ("lt", "Lithuanian", "Lietuviškai"),
    ("hu", "Hungarian", "Magyar"),
    ("nl", "Dutch", "Nederlands"),
    ("no", "Norwegian", "Norsk"),
    ("pl", "Polish", "Polski"),
    ("pt-BR", "Portuguese, Brazilian", "Português do Brasil"),
    ("ro", "Romanian, Romania", "Română"),
    ("fi", "Finnish", "Suomi"),
    ("sv-SE", "Swedish", "Svenska"),
    ("vi", "Vietnamese", "Tiếng Việt"),
    ("tr", "Turkish", "Türkçe"),
    ("cs", "Czech", "Čeština"),
    ("el", "Greek", "Ελληνικά"),
    ("bg", "Bulgarian", "български"),
    ("ru", "Russian", "Pусский"),
    ("uk", "Ukrainian", "Українська"),
    ("hi", "Hindi", "हिन्दी"),
    ("th", "Thai", "ไทย"),
    ("zh-CN", "Chinese China", "中文"),
    ("ja", "Japanese", "日本語"),
    ("zh-TW", "Chinese Taiwan", "繁體中文"),
    ("ko", "Korean", "한국어"),
]


@attrs.define
class LocaleInfo:
    symbol: str
    name: str
    native_name: str


class Localizations:
    VALID_LOCALES: dict[str, LocaleInfo] = {locale[0]: LocaleInfo(*locale) for locale in LOCALE_TUPLES}

    final_data: dict[str, str] = {}

    @classmethod
    def from_dict(cls, data: dict[str, str], /) -> "Localizations":
        (inst := cls()).final_data = data
        return inst

    def add_language(self, lang: str, value: str) -> "Localizations":
        self.final_data[lang] = value
        return self

    @classmethod
    def _check_is_valid(self, local: str) -> str:
        assert local in self.VALID_LOCALES.keys()
        return local
