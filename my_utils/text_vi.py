from typing import Text

from pyvi.ViUtils import remove_accents


def no_accent(text: Text) -> Text:
    return remove_accents(text).decode('utf-8')
