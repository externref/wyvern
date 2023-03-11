# MIT License

# Copyright (c) 2022 Sarthak

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
    def _check_is_valid(cls, local: str) -> str:
        assert local in cls.VALID_LOCALES.keys()
        return local
