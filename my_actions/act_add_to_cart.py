from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.quick_replies_template import QuickReplyElement, QuickReplies
from my_models.color import Color
from my_models.detail_shoe import DetailShoe
from my_models.shoe import Shoe
from my_models.user import User
from my_utils import SqlUtils, debug
from my_utils.entitie_name import Entities
from my_utils.error_code import ErrorCode
from my_web_setting.my_web_url import MyWebApi


class ActionAddToCart(Action):
    def name(self) -> Text:
        return 'act_add_to_cart'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Trả về generic template san pham cuoi va ask them vao gio hang/thanh toan

        :param dispatcher:
        :param tracker:
        :param domain:
        :return:
        """
        # debug('\n_________act_shoe_new_shoe_________')
        print('_____' + self.name())

        prefix_name = tracker.get_slot(Entities.prefix_name)
        customer_name = tracker.get_slot(Entities.customer_name)
        customer_id = tracker.current_state()["sender_id"]
        bot_position = tracker.get_slot(Entities.bot_position)

        shoe_id = tracker.get_slot(Entities.shoe_id)
        shoe_model = tracker.get_slot(Entities.shoe_model)
        shoe_size = tracker.get_slot(Entities.shoe_size)
        color_id = tracker.get_slot(Entities.color_id)
        color_name = tracker.get_slot(Entities.shoe_color)

        # get user id by messenger id
        query = f'''
            select id as user_id from account_user where messengerId = {customer_id}; 
        '''
        users = SqlUtils.get_result(query, User)

        if len(users) == 0:
            # chua tao tai khoan cho user
            err_code = ErrorCode.ERR_IN_ACT_ADD_TO_CARD
            err_message = f'Xin lỗi {prefix_name}{customer_name}, hệ thống đã xảy ra lỗi. Không thể thêm vào giỏ hàng.' \
                          f' error code={err_code}'
            dispatcher.utter_message(text=err_message)
            return []

        # neu them vao gio hang ma chua chon size, color thi chon size, color mac dinh
        if shoe_size is None or color_id is None:
            query = f'''
            select
                mainapp_shoe.shoeName,
                mainapp_shoe.shoeThumbnail,
                mainapp_shoe.image_static,
                mainapp_detailshoe.newPrice,
                mainapp_detailshoe.size,
                mainapp_color.colorName,
                mainapp_color.id as color_id
            from mainapp_detailshoe
                inner join mainapp_shoe
                    on (mainapp_shoe.id = mainapp_detailshoe.shoe_id)
                inner join mainapp_color
                    on (mainapp_color.id = mainapp_detailshoe.color_id)
            where
                mainapp_shoe.active = 1 and
                mainapp_detailshoe.quantityAvailable > 0 and
                mainapp_shoe.id = 8
            ;
            '''
            detail_shoes, shoes, colors = SqlUtils.get_result(query, DetailShoe, Shoe, Color)
            if len(detail_shoes) > 0:
                shoe_size = detail_shoes[0].size
                color_id = colors[0].color_id

        user = users[0]
        debug.debug_print_content('________act add to cart________')
        debug.debug_print_content(f'user id: {user.user_id}')
        debug.debug_print_content(f'color id: {color_id}')
        debug.debug_print_content(f'size id: {shoe_size}')
        result = MyWebApi.add_to_cart(user.user_id, shoe_id, color_id, shoe_size)
        debug.debug_print_content(f'result: {result}')
        if result.status_code == 201:
            text = 'Thêm vào giỏ hàng thành công'
        else:
            text = 'Thêm vào giỏ hàng thất bại'
        dispatcher.utter_message(text=text)

        # xem tiep
        quick_reply_elements = [
            QuickReplyElement(QuickReplyElement.TEXT, 'Xem giỏ hàng', 'cho xem giỏ hàng'),
            QuickReplyElement(QuickReplyElement.TEXT, 'Đặt hàng luôn', 'đặt hàng luôn'),
            QuickReplyElement(QuickReplyElement.TEXT, 'Xem lại menu', 'tôi muốn xem menu'),
        ]
        quick_replies = QuickReplies(text_before_template='Tùy chọn khác',
                                     list_quick_reply_elements=quick_reply_elements)
        # dispatcher.utter_message(json_message=quick_replies.to_json_message())
        return []
