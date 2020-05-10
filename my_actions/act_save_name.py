from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from my_utils.debug import debug
from my_utils.entitie_name import Entities
from my_utils.text_vi import remove_accents


class ActionSaveName(Action):
    def name(self) -> Text:
        return 'act_save_name'

    def run(self, dispatcher: CollectingDispatcher
            , tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        prefix_name = next(tracker.get_latest_entity_values(Entities.prefix_name), None)
        customer_name = next(tracker.get_latest_entity_values(Entities.customer_name), None)

        # correct prefix name
        if prefix_name is not None and prefix_name.strip() != '':
            prefix_name = prefix_name.strip().lower()

        if prefix_name is None or remove_accents(prefix_name) in ['tao', 'tui', 'tiu', 'to', 'minh', 'em', 'chau', ]:
            prefix_name = 'bạn'
            bot_position = 'mình'
        elif remove_accents(prefix_name) in ['anh', 'chi', 'a', 'c']:
            bot_position = 'em'
        elif remove_accents(prefix_name) in ['co', 'chu', 'bac', 'ong', 'ba', 'di', 'gi', 'cau', 'cu']:
            bot_position = 'cháu'
        else:
            prefix_name = 'bạn'
            bot_position = 'mình'

        # correct customer's name
        if customer_name is not None and customer_name.strip() != '':
            customer_name = ' ' + customer_name.strip().title()
        else:
            customer_name = ''

        debug('\n_________action_save_name_________')
        debug('prefix_name', prefix_name)
        debug('customer_name', customer_name)
        debug('bot_position', bot_position)
        debug()

        return [SlotSet(Entities.prefix_name, prefix_name),
                SlotSet(Entities.customer_name, customer_name),
                SlotSet(Entities.bot_position, bot_position)]
