from typing import Dict, List

from my_fb_api.base_api import BaseTemplate
from my_fb_api.button import Button


class ButtonTemplate(BaseTemplate):
    """
    https://developers.facebook.com/docs/messenger-platform/send-messages/template/button

    data = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "What do you want to do next?",
                "buttons": [
                    {
                        "type": "web_url",
                        "url": "https://www.messenger.com",
                        "title": "Visit Messenger"
                    },...
                ]
            }
        }
    }
    """

    def __init__(self, text: str, list_buttons: List[Button]):
        self.text = text
        self.list_buttons = list_buttons

    def to_json_message(self) -> Dict:
        buttons = []
        if self.list_buttons:
            for button in self.list_buttons:
                if isinstance(button, Button):
                    buttons.append(button.to_dict())
                elif isinstance(button, dict):
                    buttons.append(button)
                else:
                    raise TypeError('Type error. Type must be Button or Dict')
        data = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "What do you want to do next?",
                    "buttons": buttons
                }
            }
        }
        return data
