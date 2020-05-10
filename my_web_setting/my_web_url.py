from time import time

import requests

GLOBAL_URL = ' http://127.0.0.1:8000' \
    .strip()

# GLOBAL_URL = ' https://81cc819c.ngrok.io' \
#     .strip()

API_KEY = "123@abc"


class MyWebUrl:
    MEDIA = 'media'
    DETAIL_SHOE = 'product_detail'

    @staticmethod
    def get_shoe_image_url(shoe_image):
        return '/'.join([GLOBAL_URL, MyWebUrl.MEDIA, shoe_image]) + '?time=' + str(time())

    @staticmethod
    def get_detail_shoe_url(id_shoe):
        return '/'.join([GLOBAL_URL, MyWebUrl.DETAIL_SHOE, str(id_shoe)])

    @staticmethod
    def get_color_image(color_name):
        return '/'.join([GLOBAL_URL, MyWebUrl.MEDIA, color_name]) + '?time=' + str(time())

    @staticmethod
    def get_buy_now_url(messenger_id, detail_shoe_id):
        return f'{GLOBAL_URL}/cart/{messenger_id}/{detail_shoe_id}/'


class MyWebApi:
    CREATE_MESSENGER_USER_ENDPOINT = GLOBAL_URL + '/api/api_account/register_messenger_user/'
    ADD_TO_CART_ENDPOINT = GLOBAL_URL + '/api/api_cart/add_to_cart/'
    GET_USER_INFO_ENDPOINT = GLOBAL_URL + '/api/api_account/get_user_info/'
    GET_ALL_COUPONS_ENDPOINT = GLOBAL_URL + '/api/api_coupon/get_all_coupons_available/'
    GET_COUPON_INFO = GLOBAL_URL + '/api/api_coupon/get_coupon_info/'

    @staticmethod
    def create_messenger_user(messenger_id, display_name):
        data = {
            "messengerId": messenger_id,
            "displayName": display_name,
            "key": API_KEY
        }
        return requests.post(MyWebApi.CREATE_MESSENGER_USER_ENDPOINT, json=data)

    @staticmethod
    def add_to_cart(user_id, shoe_id, color_id, size):
        data = {
            "user_id": user_id,
            "shoe_id": shoe_id,
            "color_id": color_id,
            "size": size,
            "key": API_KEY
        }
        return requests.post(MyWebApi.ADD_TO_CART_ENDPOINT, json=data)

    @staticmethod
    def get_user_info(messenger_id):
        json = {
            "messengerId": messenger_id,
            "key": API_KEY
        }

        return requests.post(url=MyWebApi.GET_USER_INFO_ENDPOINT, json=json)

    @staticmethod
    def get_coupon_info(coupon_id):
        json = {'coupon_id': coupon_id}
        return requests.post(url=MyWebApi.GET_COUPON_INFO, json=json)

    @staticmethod
    def get_all_coupons_available():
        return requests.get(url=MyWebApi.GET_ALL_COUPONS_ENDPOINT)
