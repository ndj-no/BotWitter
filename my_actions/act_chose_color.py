from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.HorizontalTemplate import HorizontalTemplateElement, HorizontalTemplate
from my_fb_api.QuickRepliesTemplate import QuickReplyElement, QuickReplies
from my_fb_api.button import PostBackButton, UrlButton
from my_models.detail_shoe import DetailShoe
from my_models.shoe import Shoe
from my_utils import SqlUtils
from my_utils.debug import debug
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
        Trả về generic template 6 sản phẩm hot + quick replies đòi xem thêm

        :param dispatcher:
        :param tracker:
        :param domain:
        :return:
        """
        debug('__________act_chose_color___________')

        prefix_name = tracker.get_slot(Entities.customer_name)
        customer_name = tracker.get_slot(Entities.customer_name)
        bot_position = tracker.get_slot(Entities.bot_position)
        shoe_id = tracker.get_slot(Entities.shoe_id)
        shoe_model = tracker.get_slot(Entities.shoe_id)

        if shoe_model is None and shoe_id is None:
            err_message = f'Xin lỗi {customer_name}, {prefix_name} chưa chọn giày.'
            dispatcher.utter_message(text=err_message)
            return []

        if shoe_model:
            query = f'call get_colors_by_model({shoe_model})'
        else:
            query = f'call get_colors({shoe_id})'
        debug(query)

        shoes = SqlUtils.get_result(query, Shoe)
        detail_shoes = SqlUtils.get_result(query, DetailShoe)
        if len(detail_shoes) == 0 or len(shoes) == 0:
            err_code = ErrorCode.ERR_IN_ACT_GET_NEW_SHOE
            err_message = f'Xin lỗi {prefix_name}{customer_name}, hệ thống đã xảy ra lỗi. error={ErrorCode.ERR_IN_ACT_CHOSE_COLOR}'
            dispatcher.utter_message(text=err_message)
        else:
            horizontal_template_elements = []

            # xem tiep
            quick_reply_elements = [
                QuickReplyElement(QuickReplyElement.TEXT, 'Xem thêm', 'còn đôi nào khác k?'),
                QuickReplyElement(QuickReplyElement.TEXT, 'Xem lại menu', 'tôi muốn xem menu'),
            ]
            quick_replies = QuickReplies(text_before_template='Tùy chọn khác',
                                         list_quick_reply_elements=quick_reply_elements)
            dispatcher.utter_message(json_message=quick_replies.to_json_message())

            # print('*****************************************************')
            print(horizontal_template.to_json_message())
            # print('*****************************************************')
            # pprint(quick_replies.to_json_message())
        return []
