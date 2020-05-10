from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from my_utils import SqlUtils
from my_utils.debug import debug
from my_utils.entitie_name import Entities
from my_utils.text_vi import remove_accents
from my_models.color import Color


class ActionSetColorId(Action):
    def name(self) -> Text:
        return 'act_set_color_id'

    def run(self, dispatcher: CollectingDispatcher
            , tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        shoe_color = next(tracker.get_latest_entity_values(Entities.shoe_color), None)

        color_id = Color.get_id_by_color_name(shoe_color)

        if color_id is not None:
            color_id = str(color_id)
            return [SlotSet(Entities.color_id, color_id)]
        else:
            return []
