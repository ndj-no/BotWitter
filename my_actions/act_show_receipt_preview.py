import time
from typing import Dict, List, Text, Any

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.receipt_template import ReceiptElementPreview, ReceiptTemplatePreview
from my_models.cart import Cart
from my_models.color import Color
from my_models.coupon import Coupon
from my_models.detail_shoe import DetailShoe
from my_models.shoe import Shoe
from my_models.user import User
from my_utils.SqlUtils import get_result
from my_utils.entitie_name import Entities
from my_web_setting.my_web_url import MyWebApi


class ActionShowReceiptPreview(Action):
    def name(self) -> Text:
        return "act_show_receipt_preview"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('_____' + self.name())

        messenger_id = tracker.current_state()['sender_id']
        coupon_id = tracker.get_slot(Entities.coupon_id)

        user_api_result = MyWebApi.get_user_info(messenger_id)
        coupon_api_result = MyWebApi.get_coupon_info(coupon_id=coupon_id)

        if user_api_result.status_code == 200:
            user = User(user_api_result.json())
            # print(user.__dict__)
        else:
            dispatcher.utter_message(text='Lỗi khi call user api')
            return []

        if coupon_api_result.status_code == 200:
            coupon = Coupon(coupon_api_result.json())
        else:
            coupon = Coupon({})
            coupon.discountRate = 0

        query = f"""
                select
                    mainapp_shoe.shoeName,
                    mainapp_shoe.shoeThumbnail,
                    mainapp_shoe.image_static,
                    mainapp_detailshoe.newPrice,
                    mainapp_detailshoe.size,
                    mainapp_color.colorName,
                    cart_cart.quantityOnCart
                from cart_cart
                    inner join mainapp_detailshoe
                        on (cart_cart.detailShoe_id = mainapp_detailshoe.id)
                    inner join mainapp_shoe
                        on (mainapp_shoe.id = mainapp_detailshoe.shoe_id)
                    inner join mainapp_color
                        on (mainapp_color.id = mainapp_detailshoe.color_id)
                where
                    cart_cart.user_id = {user.user_id} and
                    mainapp_shoe.active = 1 and
                    mainapp_detailshoe.quantityAvailable > 0 and
                    cart_cart.quantityOnCart <= mainapp_detailshoe.quantityAvailable
                ;
            """

        shoes, detail_shoes, colors, carts = get_result(query, Shoe, DetailShoe, Color, Cart)
        receipt_elements = []
        for index in range(len(shoes)):
            shoe = shoes[index]
            detail_shoe = detail_shoes[index]
            color = colors[index]
            cart = carts[index]
            element = ReceiptElementPreview(shoe=shoe, detail_shoe=detail_shoe, color=color, cart=cart)
            receipt_elements.append(element)

        receipt_template_preview = ReceiptTemplatePreview(user=user, receipt_elements=receipt_elements, coupon=coupon)

        dispatcher.utter_message(text='gg', json_message=receipt_template_preview.to_json_message())

        print('_______receipt preview')
        # print(receipt_template_preview.to_json_message())
        return []
