from typing import Text, List, Dict

from my_fb_api.base_api import BaseElement, BaseTemplate
from my_fb_api.button import Button, UrlButton
from my_web_setting.my_web_url import MyWebUrl


class HorizontalTemplateElement(BaseElement):
    """
    "elements": [
            {
            "title": "Welcome!",
            "image_url": "https://petersfancybrownhats.com/company_image.png",
            "subtitle": "We have the right hat for everyone.",
            "default_action": {
                "type": "web_url",
                "url": "https://petersfancybrownhats.com/view?item=103",
                "webview_height_ratio": "tall",
            },
            "buttons": [
                {
                    "type": "web_url",
                    "url": "https://petersfancybrownhats.com",
                    "title": "View Website"
                }, {
                    "type": "postback",
                    "title": "Start Chatting",
                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                }
            ]
        }
    ]
    """

    def __init__(self,
                 image_url: Text,
                 title: Text,
                 subtitle: Text,
                 default_action,
                 list_buttons):
        self.image_url = image_url
        self.title = title
        self.subtitle = subtitle
        self.default_action = default_action
        self.list_buttons = list_buttons

    def to_dict(self) -> Dict:
        list_buttons = []
        if self.list_buttons:
            for button in self.list_buttons:
                if isinstance(button, Button):
                    list_buttons.append(button.to_dict())
                elif isinstance(button, dict):
                    list_buttons.append(button)
                else:
                    raise TypeError('invalid type button. Button or Dict only')
        if isinstance(self.default_action, HorizontalTemplateElement.DefaultAction):
            default_action = self.default_action.to_dict()
        elif isinstance(self.default_action, dict):
            default_action = self.default_action
        else:
            raise TypeError('Default Action invalid. Must be Button or Dict')
        element = {
            "title": self.title,
            "image_url": self.image_url,
            "subtitle": self.subtitle,
            "default_action": default_action,
            "buttons": list_buttons
        }
        return element

    class DefaultAction:
        def __init__(self, url: str):
            self.url = url

        def to_dict(self) -> Dict:
            return {
                "type": "web_url",
                "url": self.url,
                "webview_height_ratio": "tall",
            }


class HorizontalTemplate(BaseTemplate):
    """
    also known as generic template
    https://developers.facebook.com/docs/messenger-platform/send-messages/template/generic

    "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Welcome!",
                            "image_url": "https://petersfancybrownhats.com/company_image.png",
                            "subtitle": "We have the right hat for everyone.",
                            "default_action": {
                                "type": "web_url",
                                "url": "https://petersfancybrownhats.com/view?item=103",
                                "webview_height_ratio": "tall",
                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": "https://petersfancybrownhats.com",
                                    "title": "View Website"
                                }, {
                                    "type": "postback",
                                    "title": "Start Chatting",
                                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    """

    def __init__(self,
                 list_horizontal_template_elements):
        self.list_horizontal_template_elements = list_horizontal_template_elements

    def to_json_message(self) -> Dict:
        list_elements = []
        if self.list_horizontal_template_elements:
            for element in self.list_horizontal_template_elements:
                if isinstance(element, HorizontalTemplateElement):
                    list_elements.append(element.to_dict())
                elif isinstance(element, dict):
                    list_elements.append(element)
                else:
                    raise TypeError('Invalid type. horizontal element must be Template Element or Dict')

        message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": list_elements
                }
            }
        }
        return message
