from time import time

global_url = 'https://b3738547.ngrok.io' \
    .strip()


class MyWebUrl:
    MEDIA = 'media'
    DETAIL_SHOE = 'product_detail'

    @staticmethod
    def get_shoe_image_url(shoe_image):
        return '/'.join([global_url, MyWebUrl.MEDIA, shoe_image]) + '?time=' + str(time())

    @staticmethod
    def get_detail_shoe_url(id_shoe):
        return '/'.join([global_url, MyWebUrl.DETAIL_SHOE, str(id_shoe)])
