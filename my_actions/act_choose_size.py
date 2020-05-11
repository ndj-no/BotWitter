from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.QuickRepliesTemplate import QuickReplyElement, QuickReplies
from my_models.detail_shoe import DetailShoe
from my_utils import SqlUtils
from my_utils.debug import debug_print_content
from my_utils.entitie_name import Entities
from my_utils.error_code import ErrorCode


class ActionChooseSize(Action):
    def name(self) -> Text:
        return 'act_choose_size'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """
        Trả về quick replies sizes

        :param dispatcher:
        :param tracker:
        :param domain:
        :return:
        """
        debug_print_content('__________act_choose_size___________')

        prefix_name = tracker.get_slot(Entities.prefix_name)
        customer_name = tracker.get_slot(Entities.customer_name)
        bot_position = tracker.get_slot(Entities.bot_position)
        shoe_id = tracker.get_slot(Entities.shoe_id)
        shoe_model = tracker.get_slot(Entities.shoe_model)
        shoe_color = tracker.get_slot(Entities.shoe_color)
        color_id = tracker.get_slot(Entities.shoe_id)

        # have not chosen shoe yet
        if shoe_model is None and shoe_id is None:
            err_message = f'Xin lỗi {customer_name}, {prefix_name} chưa chọn giày.'
            dispatcher.utter_message(text=err_message)
            return []

        if color_id:
            # noinspection SqlNoDataSourceInspection
            query = f'''
                        select size 
                        from mainapp_shoe 
                            inner join mainapp_detailshoe
                                on mainapp_detailshoe.shoe_id = mainapp_shoe.id
                            where mainapp_shoe.id = {shoe_id} 
                                and mainapp_detailshoe.color_id = {color_id}
                                and mainapp_detailshoe.quantityAvailable > 0;  
                    '''

        debug_print_content('query: ' + query)

        detail_shoes = SqlUtils.get_result(query, DetailShoe)

        if len(detail_shoes) == 0:
            err_code = ErrorCode.ERR_IN_ACT_CHOSE_SIZE
            err_message = f'Xin lỗi {prefix_name}{customer_name}, hệ thống đã xảy ra lỗi. error={err_code}'
            dispatcher.utter_message(text=err_message)
            return []

        quick_reply_elements = []
        for detail_shoe in detail_shoes:
            quick_reply_elements.append(
                QuickReplyElement(
                    content_type=QuickReplyElement.TEXT,
                    title=str(detail_shoe.size),
                    payload=f'mình lấy size {detail_shoe.size}',
                )
            )

        if len(detail_shoes) == 1 and shoe_color:
            text = f'Bên {bot_position} màu {shoe_color} chỉ còn size này thôi {prefix_name} ạ:'
        elif len(detail_shoes) == 1:
            text = f'Đôi {shoe_model} chỉ còn size này thôi {prefix_name} ạ:'
        else:
            text = f'Mời {prefix_name} chọn size:'.capitalize()
        quick_replies = QuickReplies(text_before_template=text,
                                     list_quick_reply_elements=quick_reply_elements)
        dispatcher.utter_message(json_message=quick_replies.to_json_message())
        debug_print_content('quick_replies')
        debug_print_content(quick_replies.to_json_message())

        return []
