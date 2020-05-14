from abc import abstractmethod
from typing import Dict

from my_fb_api.base_api import BaseElement


class Button(BaseElement):
    def __init__(self):
        self.title = None
        self.action_value = None

    @abstractmethod
    def to_dict(self) -> Dict:
        raise NotImplementedError('You did not implement Button.to_dict() method')


class PostBackButton(Button):
    def __init__(self, title, str_send_to_webhook):
        super().__init__()
        self.title = title
        self.action_value = str_send_to_webhook

    def to_dict(self) -> Dict:
        button = {
            "type": 'postback',
            "title": self.title,
            "payload": self.action_value,
        }
        return button


class UrlButton(Button):
    COMPACT = 'compact'
    TALL = 'tall'
    FULL = 'full'

    def __init__(self, title, url_access, webview_height_ratio=TALL):
        super().__init__()
        self.title = title
        self.action_value = url_access
        self.webview_height_ratio = webview_height_ratio

    def to_dict(self) -> Dict:
        button = {
            "type": "web_url",
            "url": self.action_value,
            "title": self.title,
            # "messenger_extensions": True,
            "webview_height_ratio": self.webview_height_ratio
        }
        return button
