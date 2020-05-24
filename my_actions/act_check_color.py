from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.quick_replies_template import QuickReplyElement, QuickReplies
from my_models.color import Color
from my_models.detail_shoe import DetailShoe
from my_utils import SqlUtils
from my_utils.debug import debug_print_content
from my_utils.entitie_name import Entities
from my_utils.error_code import ErrorCode
from my_web_setting.my_web_url import MyWebUrl


class ActionCheckColor(Action):
    def name(self) -> Text:
        return 'act_check_color'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        prefix_name = tracker.get_slot(Entities.prefix_name)
        customer_name = tracker.get_slot(Entities.customer_name)
        bot_position = tracker.get_slot(Entities.bot_position)
        shoe_id = tracker.get_slot(Entities.shoe_id)
        shoe_model = tracker.get_slot(Entities.shoe_model)
        shoe_size = tracker.get_slot(Entities.shoe_size)
        color_id = tracker.get_slot(Entities.color_id)

        # have not chosen shoe yet
        if shoe_model is None and shoe_id is None:
            err_message = '{}, {} hãy chọn giày trước khi chọn màu.'.format(prefix_name, customer_name)
            dispatcher.utter_message(text=err_message)
            return [FollowupAction('act_show_menu')]

        query = f'''
            select size 
            from mainapp_shoe 
                inner join mainapp_detailshoe
                    on mainapp_detailshoe.shoe_id = mainapp_shoe.id
                where mainapp_shoe.id = {shoe_id} 
                    and mainapp_detailshoe.color_id = {color_id}
                    and mainapp_detailshoe.quantityAvailable > 0;  
        '''

        # debug_print_content('query: ' + query)

        detail_shoes = SqlUtils.get_result(query, DetailShoe)

        if len(detail_shoes) == 0:
            err_message = f'Xin lỗi {prefix_name}{customer_name}, màu này hiện không có hàng ạ.'
            dispatcher.utter_message(text=err_message)
            return [FollowupAction('act_choose_color')]
        return [FollowupAction('act_choose_size')]
