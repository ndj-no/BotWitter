from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.receipt_template import ReceiptElement, ReceiptTemplate
from my_models.cart import Cart
from my_models.color import Color
from my_models.coupon import Coupon
from my_models.detail_shoe import DetailShoe
from my_models.order_item import OrderItem
from my_models.order_package import OrderPackage
from my_models.shoe import Shoe
from my_models.user import User
from my_utils import SqlUtils
from my_utils.SqlUtils import get_result
from my_utils.debug import debug
from my_utils.entitie_name import Entities
from my_web_setting.my_web_url import MyWebApi


class ActionPlaceOrder(Action):
    """
    place order and show the receipt
    """

    def name(self) -> Text:
        return 'act_place_order'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('_____' + self.name())

        prefix_name = tracker.get_slot(Entities.prefix_name)
        customer_name = tracker.get_slot(Entities.customer_name)
        bot_position = tracker.get_slot(Entities.bot_position)
        messenger_id = tracker.current_state()['sender_id']
        coupon_id = tracker.get_slot(Entities.coupon_id)

        user_api_result = MyWebApi.get_user_info(messenger_id)
        if user_api_result.status_code == 200:
            user = User(user_api_result.json())
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
            if len(shoes) == 0:
                dispatcher.utter_message(text='Giỏ hàng của {} chưa có gì.'.format(prefix_name))
                return []
        else:
            dispatcher.utter_message(text='Lỗi khi call user api')
            return []

        api_result = MyWebApi.place_order(messenger_id, coupon_id=coupon_id)

        debug('\n_________act place order_________')
        debug('status code: {}'.format(api_result.status_code))
        if api_result.status_code != 200:
            dispatcher.utter_message(
                f'Xin lỗi {prefix_name}{customer_name}, đặt hàng không thành công. Mã lỗi: ' + api_result.status_code)
            return []

        package_id = api_result.json()['orderPackage_id']
        # package_id = 10

        query_element = f'''
            select 
                mainapp_shoe.shoeName,
                mainapp_shoe.shoeModel,
                mainapp_shoe.shoeThumbnail,
                mainapp_shoe.image_static,
                mainapp_detailshoe.size,
                mainapp_color.colorName,
                order_orderitem.itemPrice,
                order_orderitem.quantity
            from order_orderitem
                inner join mainapp_detailshoe
                    on (mainapp_detailshoe.id = order_orderitem.detailShoe_id)
                inner join mainapp_shoe
                    on (mainapp_detailshoe.shoe_id = mainapp_shoe.id)
                inner join mainapp_color
                    on (mainapp_color.id = mainapp_detailshoe.color_id)
            where
                order_orderitem.orderPackage_id = {package_id}
            ;
        '''

        shoes, detail_shoes, colors, order_items = SqlUtils.get_result(query_element, Shoe, DetailShoe, Color,
                                                                       OrderItem)

        query_package_info = f"""
            select 
                order_orderpackage.id as orderPackage_id,
                order_orderpackage.receiver,
                order_orderpackage.receiverNumber,
                order_orderpackage.receiverAddress,
                order_orderpackage.dateOrder,
                order_orderpackage.dateDelivery,
                order_orderpackage.totalPayment,
                coupon_coupon.discountRate,
                coupon_coupon.discountAmount
            from order_orderpackage
                inner join coupon_coupon
                    on (order_orderpackage.coupon_id = coupon_coupon.id)
                inner join account_user
                    on (account_user.id = order_orderpackage.user_id)
            where
                order_orderpackage.id = {package_id}
            ;
            """

        coupons, order_packages = SqlUtils.get_result(query_package_info, Coupon, OrderPackage)

        receipt_elements = []
        for index in range(len(shoes)):
            shoe = shoes[index]
            detail_shoe = detail_shoes[index]
            color = colors[index]
            order_item = order_items[index]
            element = ReceiptElement(shoe, detail_shoe, color, order_item)
            receipt_elements.append(element)

        order_package = order_packages[0]
        coupon = coupons[0]
        receipt_template = ReceiptTemplate(order_package=order_package, coupon=coupon,
                                           receipt_elements=receipt_elements)
        dispatcher.utter_message(json_message=receipt_template.to_json_message())
        dispatcher.utter_message(
            text='Đã đặt hàng thành công. Cảm ơn {}{} đã sử dụng dịch vụ của Witter Shoe'.format(prefix_name,
                                                                                                 customer_name))
        dispatcher.utter_message(
            'Đơn hàng này dự kiến giao vào ngày {} nhé {}'.format(str(order_package.dateDelivery).split(' ')[0],
                                                                  prefix_name))
        return []
