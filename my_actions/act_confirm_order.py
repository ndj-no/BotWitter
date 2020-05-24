from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.quick_replies_template import QuickReplies, QuickReplyElement


class ActionConfirmOrder(Action):
    def name(self) -> Text:
        return 'act_confirm_order'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('_____' + self.name())

        quick_reply_elements = [
            # text on screen and the text send back to server
            QuickReplyElement(QuickReplyElement.TEXT, 'OK', 'ok'),
            QuickReplyElement(QuickReplyElement.TEXT, 'Không', 'không'),
        ]

        quick_replies = QuickReplies(
            text_before_template='Vui lòng xác nhận:',
            list_quick_reply_elements=quick_reply_elements
        )

        dispatcher.utter_message(json_message=quick_replies.to_json_message())
        return []
