from pprint import pprint
from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.QuickRepliesTemplate import QuickReplies, QuickReplyElement


class ActionTestAnything(Action):
    def name(self) -> Text:
        return 'act_test_anything'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        quick_reply_elements = [
            QuickReplyElement(QuickReplyElement.TEXT, 'xem giày mới', 'mới nhập'),
            QuickReplyElement(QuickReplyElement.TEXT, 'xem giày đang hot', 'đang hot'),
            QuickReplyElement(QuickReplyElement.TEXT, 'bạn có giày gì?', 'bạn có giày gì?'),
            QuickReplyElement(QuickReplyElement.TEXT, 'có mã giảm giá k bạn?', 'có mã giảm giá k bạn?'),
            QuickReplyElement(QuickReplyElement.TEXT, 'hướng dẫn sử dụng', 'help'),
            QuickReplyElement(QuickReplyElement.TEXT, 'k có gì', 'nope'),
        ]

        quick_replies = QuickReplies(text='Xin hãy chọn một nội dung:',
                                     list_quick_reply_element_objs=quick_reply_elements)

        dispatcher.utter_message(json_message=quick_replies.to_json_message())
        print(quick_replies.to_json_message())
        return []
