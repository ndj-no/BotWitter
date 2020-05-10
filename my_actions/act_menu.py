from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.QuickRepliesTemplate import QuickReplies, QuickReplyElement


class ActionIntroduce(Action):
    def name(self) -> Text:
        return 'act_menu'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        quick_reply_elements = [
            # text on screen and the text send back to server
            QuickReplyElement(QuickReplyElement.TEXT, 'Xem giày mới nhập', 'có đôi nào mới ra k?'),
            QuickReplyElement(QuickReplyElement.TEXT, 'Xem giày đang hot', 'cho a xem vài đôi giày đang hot đi'),
            QuickReplyElement(QuickReplyElement.TEXT, 'Bạn có giày gì?', 'bạn có giày gì?'),
            QuickReplyElement(QuickReplyElement.TEXT, 'Có mã giảm giá nào k?', 'có mã giảm giá k bạn?'),
            QuickReplyElement(QuickReplyElement.TEXT, 'Hướng dẫn sử dụng', 'help'),
            QuickReplyElement(QuickReplyElement.TEXT, 'K có gì', 'nope'),
        ]

        quick_replies = QuickReplies(
            text_before_template='Xin hãy một nội dung bên dưới:',
            list_quick_reply_elements=quick_reply_elements
        )

        dispatcher.utter_message(json_message=quick_replies.to_json_message())
        return []
