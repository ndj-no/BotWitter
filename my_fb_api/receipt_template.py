import time
from datetime import datetime
from typing import Dict, List

from my_fb_api.base_api import BaseTemplate, BaseElement
from my_models.cart import Cart
from my_models.color import Color
from my_models.coupon import Coupon
from my_models.detail_shoe import DetailShoe
from my_models.order_item import OrderItem
from my_models.order_package import OrderPackage
from my_models.shoe import Shoe
from my_models.user import User
from my_web_setting.my_web_url import MyWebUrl, GLOBAL_URL


class ReceiptElementPreview(BaseElement):
    def __init__(self, shoe: Shoe, detail_shoe: DetailShoe, color: Color, cart: Cart):
        self.shoe = shoe
        self.detail_shoe = detail_shoe
        self.color = color
        self.cart = cart

    def to_dict(self) -> Dict:
        data = {
            "title": self.shoe.shoeName,
            "subtitle": f"màu: {self.color.colorName}, size: {self.detail_shoe.size}",
            "quantity": self.cart.quantityOnCart,
            "price": self.detail_shoe.newPrice,
            "currency": "VND",
            # "image_url": MyWebUrl.get_shoe_image_url(self.shoe.shoeThumbnail)
            "image_url": self.shoe.image_static
        }
        return data


class ReceiptTemplatePreview(BaseTemplate):
    def __init__(self, user: User, receipt_elements: List[ReceiptElementPreview], coupon: Coupon):
        self.user = user
        self.receipt_elements = receipt_elements
        self.coupon = coupon

    def to_json_message(self) -> Dict:
        shipping_cost = self.cal_shipping()
        total_tax = self.cal_tax()

        subtotal = 0
        elements = []
        for element in self.receipt_elements:
            detail_shoe = element.detail_shoe
            cart = element.cart
            subtotal = subtotal + detail_shoe.newPrice * cart.quantityOnCart
            elements.append(element.to_dict())

        coupon_discount_amount = int(subtotal * self.coupon.discountRate / 100)
        total_cost = subtotal - coupon_discount_amount
        if self.user.phone:
            address_1 = self.user.phone
            address_2 = self.user.defaultAddress
        elif self.user.defaultAddress:
            address_1 = self.user.defaultAddress
            address_2 = ''
        else:
            address_1 = 'Địa chỉ chưa cung cấp.'
            address_2 = ''

        adjustments = []
        if coupon_discount_amount > 0:
            adjustments = [
                {
                    "name": f"Mã giảm giá {self.coupon.discountRate}%",
                    "amount": coupon_discount_amount
                },
            ]
        message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "receipt",
                    "recipient_name": self.user.displayName,
                    "order_number": "chưa đặt hàng",
                    "currency": "VND",
                    "payment_method": "Chưa thanh toán. Thanh toán khi nhận hàng",
                    "order_url": "http://127.0.0.1:8000/order/order_history/",
                    "timestamp": str(time.time()).split('.')[0],
                    "address": {
                        "street_1": address_1,
                        "street_2": address_2,
                        "city": "_",
                        "postal_code": "_",
                        "state": "_",
                        "country": "VN"
                    },
                    "summary": {
                        "subtotal": subtotal,
                        "shipping_cost": shipping_cost,
                        "total_tax": total_tax,
                        "total_cost": total_cost
                    },
                    "adjustments": adjustments,
                    "elements": elements
                }
            }
        }
        return message

    def cal_shipping(self):
        return 0

    def cal_tax(self):
        return 0


class ReceiptElement(BaseElement):
    def __init__(self, shoe: Shoe, detail_shoe: DetailShoe, color: Color, order_item: OrderItem):
        self.shoe = shoe
        self.detail_shoe = detail_shoe
        self.color = color
        self.order_item = order_item

    def to_dict(self) -> Dict:
        data = {
            "title": self.shoe.shoeName,
            "subtitle": f"màu: {self.color.colorName}, size: {self.detail_shoe.size}",
            "quantity": self.order_item.quantity,
            "price": self.order_item.itemPrice,
            "currency": "VND",
            # "image_url": MyWebUrl.get_shoe_image_url(self.shoe.shoeThumbnail)
            "image_url": self.shoe.image_static
        }
        return data


class ReceiptTemplate(BaseTemplate):
    def __init__(self, order_package: OrderPackage, coupon: Coupon, receipt_elements: List[ReceiptElement]):
        self.order_package = order_package
        self.receipt_elements = receipt_elements
        self.coupon = coupon

    def to_json_message(self) -> Dict:
        shipping_cost = self.cal_shipping()
        total_tax = self.cal_tax()

        subtotal = 0
        elements = []
        for element in self.receipt_elements:
            subtotal = subtotal + element.order_item.itemPrice * element.order_item.quantity
            elements.append(element.to_dict())

        coupon_discount_amount = int(subtotal * self.coupon.discountRate / 100)
        total_cost = subtotal - coupon_discount_amount

        if self.order_package.receiverNumber:
            address_1 = self.order_package.receiverNumber
            address_2 = self.order_package.receiverAddress
        else:
            address_1 = self.order_package.receiverAddress
            address_2 = ''

        adjustments = []
        if coupon_discount_amount > 0:
            adjustments = [
                {
                    "name": f"Mã giảm giá {self.coupon.discountRate}%",
                    "amount": coupon_discount_amount
                },
            ]

        json = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "receipt",
                    "recipient_name": self.order_package.receiver,
                    "order_number": f"{self.order_package.orderPackage_id}",
                    "currency": "VND",
                    "payment_method": "Thanh toán khi nhận hàng",
                    "order_url": MyWebUrl.get_order_detail(self.order_package.orderPackage_id),
                    # current time
                    "timestamp": str(datetime.timestamp(self.order_package.dateOrder)).split('.')[0],
                    "address": {
                        "street_1": address_1,
                        "street_2": address_2,
                        "city": "_",
                        "postal_code": "_",
                        "state": "_",
                        "country": "VN"
                    },
                    "summary": {
                        "subtotal": subtotal,
                        "shipping_cost": shipping_cost,
                        "total_tax": total_tax,
                        "total_cost": total_cost
                    },
                    "adjustments": adjustments,
                    "elements": elements
                }
            }
        }
        # print(json)
        return json

    def cal_shipping(self):
        return 0

    def cal_tax(self):
        return 0
