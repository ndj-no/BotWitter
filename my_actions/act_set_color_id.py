from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from my_models.color import Color
from my_utils.entitie_name import Entities


class ActionSetColorId(Action):
    def name(self) -> Text:
        return 'act_set_color_id'

    def run(self, dispatcher: CollectingDispatcher
            , tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('_____' + self.name())

        shoe_color = tracker.get_slot(Entities.shoe_color)
        print(shoe_color)
        color_id = Color.get_id_by_color_name(shoe_color)
        print(color_id)
        if color_id is not None:
            return [SlotSet(Entities.color_id, color_id)]
        else:
            return []
