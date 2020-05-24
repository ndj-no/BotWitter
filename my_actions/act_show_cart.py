from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.button import PostBackButton, UrlButton
from my_fb_api.button_template import ButtonTemplate
from my_fb_api.quick_replies_template import QuickReplyElement, QuickReplies
from my_models.coupon import Coupon
from my_utils.debug import debug
from my_utils.entitie_name import Entities
from my_web_setting.my_web_url import MyWebUrl, MyWebApi


class ActionShowCart(Action):
    def name(self) -> Text:
        return 'act_show_cart'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('_____' + self.name())

        prefix_name = tracker.get_slot(Entities.prefix_name)
        messenger_id = tracker.current_state()["sender_id"]
        coupon_id = tracker.get_slot(Entities.coupon_id)
        coupon_code = tracker.get_slot(Entities.coupon_code)

        MyWebUrl.get_edit_cart_url(messenger_id)

        buttons = [
            UrlButton(title='Xem giỏ hàng', url_access=f'{MyWebUrl.get_edit_cart_url(messenger_id)}'),
            PostBackButton(title='Đặt hàng luôn', str_send_to_webhook=f'đặt hàng nào'),
        ]
        if coupon_code:
            button_template = ButtonTemplate(
                f'Hiện {prefix_name} đang có mã giảm giá {coupon_code} đó. {prefix_name} có muốn đặt hàng luôn không?',
                buttons)
        else:
            button_template = ButtonTemplate(f'Giỏ hàng của {prefix_name} đây ạ', buttons)
        dispatcher.utter_message(json_message=button_template.to_json_message())

        # xem tiep
        quick_reply_elements = [
            QuickReplyElement(QuickReplyElement.TEXT, 'Xem thêm giày', 'Xem đôi giày khác'),
        ]
        text = 'Hành động khác:'
        if not coupon_id:
            text = '{} có muốn lấy mã giảm giá không ạ?'.format(prefix_name)
            quick_reply_elements.append(
                QuickReplyElement(QuickReplyElement.TEXT, 'Lấy mã giảm giá', 'cho tôi xem mã giảm giá'),
            )
        quick_replies = QuickReplies(
            text_before_template=text,
            list_quick_reply_elements=quick_reply_elements)
        dispatcher.utter_message(json_message=quick_replies.to_json_message())

        return []
