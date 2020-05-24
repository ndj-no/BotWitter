from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher

from my_models.shoe import Shoe
from my_utils import SqlUtils
from my_utils.debug import debug
from my_utils.entitie_name import Entities


class ActionSetShoeId(Action):
    def name(self) -> Text:
        return 'act_set_shoe_id'

    def run(self, dispatcher: CollectingDispatcher
            , tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('_____' + self.name())

        shoe_model = tracker.get_slot(Entities.shoe_model)
        prefix_name = tracker.get_slot(Entities.prefix_name)
        print('gg')
        if not shoe_model:
            dispatcher.utter_message('{} chưa chọn đôi giày nào'.format(prefix_name))
            return [FollowupAction('act_shoe_menu')]
        shoe_model = str(shoe_model).upper()
        query = f'select id as shoe_id, shoeModel, shoeName from mainapp_shoe where mainapp_shoe.shoeModel like "%{shoe_model}%";'
        shoes = SqlUtils.get_result(query, Shoe)

        # debug('\n_________act_set_shoe_id_________')
        # debug('query')
        # debug(query)
        # debug('model', shoe_model)
        # debug(len(shoes), 'KQ')
        # if len(shoes) > 0:
        #     debug('shoe_id[0]', shoes[0].shoe_id)
        # debug()
        if len(shoes) > 0:
            return [SlotSet(Entities.shoe_id, str(shoes[0].shoe_id)), SlotSet(Entities.shoe_model, shoe_model)]
        else:
            return [SlotSet(Entities.shoe_model, shoe_model)]
