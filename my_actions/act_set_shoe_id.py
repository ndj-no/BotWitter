from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from my_utils import SqlUtils
from my_utils.debug import debug
from my_utils.entitie_name import Entities
from my_utils.text_vi import remove_accents
from my_models.shoe import Shoe


class ActionSetShoeId(Action):
    def name(self) -> Text:
        return 'act_set_shoe_id'

    def run(self, dispatcher: CollectingDispatcher
            , tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shoe_model = next(tracker.get_latest_entity_values(Entities.shoe_model), None)

        query = f'select id as shoe_id from {Shoe.TABLE_NAME} where {Shoe.COL_SHOE_MODEL} like "%{shoe_model}%"'
        shoes = SqlUtils.get_result(query, Shoe)

        debug('\n_________act_set_shoe_id_________')
        debug('query')
        debug(query)
        debug('model', shoe_model)
        debug(len(shoes), 'KQ')
        if len(shoes) > 0:
            debug('shoe_id[0]', shoes[0].shoe_id)
        debug()
        if len(shoes) > 0:
            return [SlotSet(Entities.shoe_id, str(shoes[0].shoe_id))]
        else:
            return []
