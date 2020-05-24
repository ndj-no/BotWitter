from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.quick_replies_template import QuickReplies, QuickReplyElement
from my_utils.entitie_name import Entities


class ActionShowMenu(Action):
    def name(self) -> Text:
        return 'act_show_menu'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('_____' + self.name())
        prefix_name = tracker.get_slot(Entities.prefix_name)
        customer_name = tracker.get_slot(Entities.customer_name)
        bot_position = tracker.get_slot(Entities.bot_position)
        quick_reply_elements = [
            # text on screen and the text send back to server
            QuickReplyElement(QuickReplyElement.TEXT, 'Bạn có giày gì?', 'bạn có giày gì?'),
            QuickReplyElement(QuickReplyElement.TEXT, 'Xem giày mới', 'có đôi nào mới ra k?'),
            QuickReplyElement(QuickReplyElement.TEXT, 'Xem giày đang hot', 'cho a xem vài đôi giày đang hot đi'),
            QuickReplyElement(QuickReplyElement.TEXT, 'Có mã giảm giá k?', 'có mã giảm giá k bạn?'),
            QuickReplyElement(QuickReplyElement.TEXT, 'Cho xem giỏ hàng', 'cho tôi xem giỏ hàng'),
            QuickReplyElement(QuickReplyElement.TEXT, 'Hướng dẫn', 'help'),
            QuickReplyElement(QuickReplyElement.TEXT, 'K có gì', 'nope'),
        ]

        quick_replies = QuickReplies(
            text_before_template=f'{prefix_name} muốn làm gì?',
            list_quick_reply_elements=quick_reply_elements
        )

        dispatcher.utter_message(json_message=quick_replies.to_json_message())
        return []
