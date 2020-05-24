from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_utils import debug
from my_utils.entitie_name import Entities
from my_web_setting.my_web_url import MyWebApi


class ActionRegisterUser(Action):
    def name(self) -> Text:
        return 'act_register_user'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('_____' + self.name())

        customer_name = tracker.get_slot(Entities.customer_name)
        customer_id = tracker.current_state()["sender_id"]

        debug.debug_print_content('________create user________')
        debug.debug_print_content(f'messenger id: {customer_id}')
        debug.debug_print_content(f'customer name: {customer_name}')
        debug.debug_print_content(MyWebApi.create_messenger_user(customer_id, str(customer_name) + str(customer_id)))
        debug.debug_print_content()
        return []
