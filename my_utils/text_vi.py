from typing import Text

from pyvi.ViUtils import remove_accents as rm_accent


def remove_accents(text: Text) -> Text:
    return rm_accent(text).decode('utf-8')
