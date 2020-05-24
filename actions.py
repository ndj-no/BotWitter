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


# do NOT optimize imports

from my_actions.act_show_cart import ActionShowCart
from my_actions.act_add2cart_or_buy_now import ActionAdd2CartOrBuyNow
from my_actions.act_add_to_cart import ActionAddToCart
from my_actions.act_choose_color import ActionChooseColor
from my_actions.act_choose_size import ActionChooseSize
from my_actions.act_check_size import ActionCheckSize
from my_actions.act_confirm_order import ActionConfirmOrder
from my_actions.act_place_order import ActionPlaceOrder
from my_actions.act_register_user import ActionRegisterUser
from my_actions.act_save_name import ActionSaveName
from my_actions.act_set_color_id import ActionSetColorId
from my_actions.act_check_color import ActionCheckColor
from my_actions.act_set_coupon_id import ActionSetCouponId
from my_actions.act_set_shoe_id import ActionSetShoeId
from my_actions.act_show_coupons import ActionShowCoupons
from my_actions.act_show_hot_shoes import ActionShowHotShoes
from my_actions.act_show_list_categories import ActionShowListCategory
from my_actions.act_show_menu import ActionShowMenu
from my_actions.act_show_new_shoes import ActionShowNewShoes
from my_actions.act_show_receipt_preview import ActionShowReceiptPreview
from my_actions.act_show_shoes_by_category import ActionShowShoesByCategory
