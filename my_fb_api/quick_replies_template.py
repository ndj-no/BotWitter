from typing import Dict, List

from my_fb_api.base_api import BaseElement, BaseTemplate


class QuickReplyElement(BaseElement):
    """
    https://developers.facebook.com/docs/messenger-platform/send-messages/quick-replies
    """

    TEXT = 'text'
    USER_PHONE_NUMBER = 'user_phone_number'
    USER_EMAIL = 'user_email'

    def __init__(self, content_type, title, payload, image_url=None):
        self.content_type = content_type
        self.title = title
        self.payload = payload
        self.image_url = image_url

    def to_dict(self) -> Dict:
        element = {
            "content_type": self.content_type,
            "title": self.title,
            "payload": self.payload,
        }
        if self.image_url:
            element["image_url"] = self.image_url
        return element


class QuickReplies(BaseTemplate):
    def __init__(self,
                 text_before_template,
                 list_quick_reply_elements):
        self.text = text_before_template if text_before_template else ''
        self.list_quick_reply_elements = list_quick_reply_elements

    def to_json_message(self):
        quick_replies = []
        if self.list_quick_reply_elements:
            for quick_reply in self.list_quick_reply_elements:
                if isinstance(quick_reply, QuickReplyElement):
                    quick_replies.append(quick_reply.to_dict())
                elif isinstance(quick_reply, dict):
                    quick_replies.append(quick_reply)
                else:
                    raise TypeError('Type invalid. Must be Quick Reply Element or Dict')

        message = {
            "text": self.text,
            "quick_replies": quick_replies,
        }
        return message
