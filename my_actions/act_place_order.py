from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.button import PostBackButton, UrlButton
from my_fb_api.button_template import ButtonTemplate
from my_fb_api.receipt_template import ReceiptElement, ReceiptTemplate
from my_models.color import Color
from my_models.coupon import Coupon
from my_models.detail_shoe import DetailShoe
from my_models.order_item import OrderItem
from my_models.order_package import OrderPackage
from my_models.shoe import Shoe
from my_utils import SqlUtils
from my_utils.debug import debug
from my_utils.entitie_name import Entities
from my_web_setting.my_web_url import MyWebUrl, MyWebApi


class ActionPlaceOrder(Action):
    """
    place order and show the receipt
    """

    def name(self) -> Text:
        return 'act_place_order'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        prefix_name = tracker.get_slot(Entities.prefix_name)
        customer_name = tracker.get_slot(Entities.customer_name)
        bot_position = tracker.get_slot(Entities.bot_position)

        messenger_id = tracker.current_state()['sender_id']
        coupon_id = tracker.get_slot(Entities.coupon_id)
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
        return []
