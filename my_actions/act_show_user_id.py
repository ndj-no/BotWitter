from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionShowUserId(Action):
    def name(self) -> Text:
        return 'act_show_user_id'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('_____' + self.name())

        user_id = tracker.sender_id

        dispatcher.utter_message(text=f'user id = {user_id}')
        return []
