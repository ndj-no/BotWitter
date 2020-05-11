# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
#
# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
# from my_models.category import Category
# from rasa_sdk.events import SlotSet
#
# from my_models.shoe import Shoe
# from my_utils.text_vi import no_accent
#
# from my_utils import SqlUtils
# from my_utils.entitie_name import Entities


from my_actions.act_show_shoes_by_category import ActionShowShoesByCategory
from my_actions.act_show_receipt import ActionShowReceipt
from my_actions.act_show_list_categories import ActionGetListCategory
from my_actions.act_save_name import ActionSaveName
from my_actions.act_test_anything import ActionTestAnything
from my_actions.act_show_menu import ActionIntroduce
from my_actions.act_show_hot_shoes import ActionShowHotShoes
from my_actions.act_show_new_shoes import ActionShowNewShoes
from my_actions.act_choose_color import ActionChooseColor
from my_actions.act_show_user_id import ActionShowUserId
