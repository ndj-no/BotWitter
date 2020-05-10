from typing import Dict, List, Text, Any

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.receipt_template import ReceiptElement, ReceiptTemplate
from my_models.cart import Cart
from my_models.color import Color
from my_models.coupon import Coupon
from my_models.detail_shoe import DetailShoe
from my_models.shoe import Shoe
from my_models.user import User
from my_utils.SqlUtils import get_result
from my_utils.entitie_name import Entities
from my_web_setting.my_web_url import MyWebApi


class ActionShowReceipt(Action):
    def name(self) -> Text:
        return "act_show_receipt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        messenger_id = tracker.current_state()['sender_id']
        coupon_id = tracker.get_slot(Entities.coupon_id)
        user_api_result = MyWebApi.get_user_info(messenger_id)
        coupon_api_result = MyWebApi.get_coupon_info(coupon_id)

        if user_api_result.status_code == 200:
            user = User(user_api_result.json())
        else:
            dispatcher.utter_message(text='Lỗi khi get user api')
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
            element = ReceiptElement(shoe=shoe, detail_shoe=detail_shoe, color=color, cart=cart)
            receipt_elements.append(element)

        receipt_template = ReceiptTemplate(user=user, receipt_elements=receipt_elements, coupon=coupon)

        dispatcher.utter_message(json_message=receipt_template.to_json_message())

        return []

# class ActionShowReceipt(Action):
#     """
#     get a list of categories
#     """
#
#     def name(self) -> Text:
#         return "act_show_receipt"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         user_id = tracker.current_state()['sender_id']
#
#         query = f'SELECT * ' \
#                 f'FROM {OrderPackage.TABLE_NAME} INNER JOIN {OrderPackage.TABLE_NAME} ' \
#                 f'on ( {User.TABLE_NAME}.id = {OrderPackage.TABLE_NAME}.user_id ) ' \
#                 f'WHERE {User.TABLE_NAME}.id = {user_id} order by '
#         get_result(query, OrderPackage)
#         message = {
#             "attachment": {
#                 "type": "template",
#                 "payload": {
#                     "template_type": "receipt",
#                     "recipient_name": "Stephane Crozatier",
#                     "order_number": "chưa đặt",
#                     "currency": "VND",
#                     "payment_method": "Visa 2345",
#                     "order_url": "http://petersapparel.parseapp.com/order?order_id=123456",
#                     "timestamp": str(time.time()).split('.')[0],
#                     "address": {
#                         "street_1": "1 Hacker Way",
#                         "street_2": "",
#                         "city": "_",
#                         "postal_code": "_",
#                         "state": "_",
#                         "country": "VN"
#                     },
#                     "summary": {
#                         "subtotal": 7500000,
#                         "shipping_cost": 0,
#                         "total_tax": 0,
#                         "total_cost": 560000
#                     },
#                     "adjustments": [
#                         {
#                             "name": "New Customer Discount",
#                             "amount": 20
#                         },
#                         {
#                             "name": "$10 Off Coupon",
#                             "amount": 10
#                         }
#                     ],
#                     "elements": [
#                         {
#                             "title": "Classic White T-Shirt",
#                             "subtitle": "100% Soft and Luxurious Cotton",
#                             "quantity": 2,
#                             "price": 50,
#                             "currency": "VND",
#                             "image_url": "https://dictionary.cambridge.org/vi/images/thumb/Tshirt_noun_001_18267.jpg"
#                         },
#                         {
#                             "title": "Classic Gray T-Shirt",
#                             "subtitle": "100% Soft and Luxurious Cotton",
#                             "quantity": 1,
#                             "price": 250000,
#                             "currency": "VND",
#                             "image_url": "https://dictionary.cambridge.org/vi/images/thumb/Tshirt_noun_001_18267.jpg"
#                         }
#                     ]
#                 }
#             }
#         }
#         user_id = (tracker.current_state())["sender_id"]
#         dispatcher.utter_message(text=str(user_id), json_message=message)
#         return []
