from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.button import PostBackButton, UrlButton
from my_fb_api.button_template import ButtonTemplate
from my_models.coupon import Coupon
from my_utils.debug import debug
from my_utils.entitie_name import Entities
from my_web_setting.my_web_url import MyWebUrl, MyWebApi


class ActionShowCoupons(Action):
    def name(self) -> Text:
        return 'act_show_coupons'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """

        :param dispatcher:
        :param tracker:
        :param domain:
        :return:
        """

        prefix_name = tracker.get_slot(Entities.prefix_name)
        customer_name = tracker.get_slot(Entities.customer_name)
        bot_position = tracker.get_slot(Entities.bot_position)

        api_result = MyWebApi.get_all_coupons_available()

        debug('\n_________act_show_coupon_________')
        debug('status code: {}'.format(api_result.status_code))
        if api_result.status_code != 200:
            dispatcher.utter_message(
                f'Xin lỗi {prefix_name}{customer_name}, đã có lỗi trên hệ thống. Mã lỗi: ' + api_result.status_code)
            return []

        coupons = []
        for element in api_result.json():
            coupons.append(Coupon(element))
        debug('{} coupons'.format(len(coupons)))
        if len(coupons) == 0:
            dispatcher.utter_message(
                f'Xin lỗi {prefix_name}{customer_name}, hiện cửa hàng không có mã giảm giá nào')
            return []

        for index, coupon in enumerate(coupons):
            buttons = [
                PostBackButton(title='Lấy mã này', str_send_to_webhook=f'tôi lấy mã {coupon.couponCode}'),
                # test button
                UrlButton(title='Chi tiết', url_access=f'{MyWebUrl.get_detail_shoe_url(0)}')
            ]
            button_template = ButtonTemplate(f'Giảm {coupon.discountRate}%', buttons)

            dispatcher.utter_message('Mã: {}'.format(coupon.couponCode))
            dispatcher.utter_message(json_message=button_template.to_json_message())
        return []
