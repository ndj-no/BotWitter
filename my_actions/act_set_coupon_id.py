from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from my_models.coupon import Coupon
from my_utils.entitie_name import Entities
from my_web_setting.my_web_url import MyWebApi


class ActionSetCouponId(Action):
    def name(self) -> Text:
        return 'act_set_coupon_id'

    def run(self, dispatcher: CollectingDispatcher
            , tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('_____' + self.name())

        # shoe_color = next(tracker.get_latest_entity_values(Entities.shoe_color), None)
        coupon_code = tracker.get_slot(Entities.coupon_code)
        prefix_name = tracker.get_slot(Entities.prefix_name)
        api_result = MyWebApi.get_coupon_info(coupon_code=coupon_code)
        if api_result.status_code == 200:
            coupon = Coupon(api_result.json())
            dispatcher.utter_message(
                'Lưu mã giảm giá thành công. Mã giảm giá sẽ được áp dụng tự động khi {} mua hàng.'.format(prefix_name))
            return [SlotSet(Entities.coupon_id, coupon.coupon_id)]
        else:
            return []
