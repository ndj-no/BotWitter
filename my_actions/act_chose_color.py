from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.HorizontalTemplate import HorizontalTemplateElement, HorizontalTemplate
from my_fb_api.QuickRepliesTemplate import QuickReplyElement, QuickReplies
from my_fb_api.button import PostBackButton, UrlButton
from my_models.color import Color
from my_models.detail_shoe import DetailShoe
from my_models.shoe import Shoe
from my_utils import SqlUtils
from my_utils.debug import debug, debug_print_content
from my_utils.entitie_name import Entities
from my_utils.error_code import ErrorCode
from my_utils.price_format import price_format
from my_web_setting.my_web_url import MyWebUrl


class ActionChoseColor(Action):
    def name(self) -> Text:
        return 'act_chose_color'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Trả về list cacs mau

        :param dispatcher:
        :param tracker:
        :param domain:
        :return:
        """
        debug_print_content('__________act_chose_color___________')

        prefix_name = tracker.get_slot(Entities.prefix_name)
        customer_name = tracker.get_slot(Entities.customer_name)
        bot_position = tracker.get_slot(Entities.bot_position)
        shoe_id = tracker.get_slot(Entities.shoe_id)
        shoe_model = tracker.get_slot(Entities.shoe_model)

        # have not chosen shoe yet
        if shoe_model is None and shoe_id is None:
            err_message = f'Xin lỗi {customer_name}, {prefix_name} chưa chọn giày.'
            dispatcher.utter_message(text=err_message)
            return []

        if shoe_id:
            query = f'call get_colors({shoe_id})'
        elif shoe_model:
            query = f'call get_colors_by_model("{shoe_model}")'
        debug_print_content('query: ' + query)

        colors = SqlUtils.get_result(query, Color)

        if len(colors) == 0:
            err_code = ErrorCode.ERR_IN_ACT_CHOSE_COLOR
            err_message = f'Xin lỗi {prefix_name}{customer_name}, hệ thống đã xảy ra lỗi. error={err_code}'
            dispatcher.utter_message(text=err_message)
            return []

        # xem tiep
        quick_reply_elements = []
        for color in colors:
            quick_reply_elements.append(
                QuickReplyElement(
                    QuickReplyElement.TEXT,
                    color.colorName,
                    f'tôi lấy màu {color.colorName} color_id {color.color_id}',
                    image_url=MyWebUrl.get_color_image('colors/red.png'))
            )
        if len(colors) == 1:
            text = f'Bên {bot_position} chỉ còn màu này thôi {prefix_name} ạ:'
        else:
            text = prefix_name.capitalize() + ' hãy chọn một màu bên dưới:'
        quick_replies = QuickReplies(text_before_template=text,
                                     list_quick_reply_elements=quick_reply_elements)
        dispatcher.utter_message(json_message=quick_replies.to_json_message())
        debug_print_content('quick_replies')
        debug_print_content(quick_replies.to_json_message())
        # print('*****************************************************')
        # print(horizontal_template.to_json_message())
        # print('*****************************************************')
        # pprint(quick_replies.to_json_message())
        return []
