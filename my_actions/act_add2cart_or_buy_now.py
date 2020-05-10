from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.HorizontalTemplate import HorizontalTemplateElement, HorizontalTemplate
from my_fb_api.QuickRepliesTemplate import QuickReplyElement, QuickReplies
from my_fb_api.button import PostBackButton, UrlButton
from my_models.color import Color
from my_models.detail_shoe import DetailShoe
from my_models.shoe import Shoe
from my_utils import SqlUtils
from my_utils.entitie_name import Entities
from my_utils.error_code import ErrorCode
from my_utils.price_format import price_format
from my_web_setting.my_web_url import MyWebUrl


class ActionAdd2CartOrBuyNow(Action):
    def name(self) -> Text:
        return 'act_add2cart_or_buy_now'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Trả về generic template san pham cuoi va ask them vao gio hang/thanh toan

        :param dispatcher:
        :param tracker:
        :param domain:
        :return:
        """
        # debug('\n_________act_shoe_new_shoe_________')

        prefix_name = tracker.get_slot(Entities.prefix_name)
        customer_name = tracker.get_slot(Entities.customer_name)
        bot_position = tracker.get_slot(Entities.bot_position)
        shoe_id = tracker.get_slot(Entities.shoe_id)
        shoe_model = tracker.get_slot(Entities.shoe_model)
        shoe_size = tracker.get_slot(Entities.shoe_size)
        color_id = tracker.get_slot(Entities.color_id)
        color_name = tracker.get_slot(Entities.shoe_color)

        # get_final_shoe(shoe_id int, shoe_size int, color_id int)
        # query = 'call get_final_shoe({}, {}, {})'.format(shoe_id, shoe_size, color_id)
        query = f'''
            select 
                mainapp_shoe.id as shoe_id,
                mainapp_shoe.shoeName,
                mainapp_shoe.shoeModel,
                mainapp_shoe.shoeThumbnail,
                mainapp_detailshoe.id as detailShoe_id,
                mainapp_detailshoe.newPrice,
                mainapp_detailshoe.quantityAvailable,
                mainapp_detailshoe.size,
                mainapp_color.id as color_id,
                mainapp_color.colorName
            from mainapp_shoe 
                inner join mainapp_detailshoe
                    on (mainapp_shoe.id = mainapp_detailshoe.shoe_id)
                inner join mainapp_color
                    on (mainapp_detailshoe.color_id = mainapp_color.id)
            where
                mainapp_shoe.id = {shoe_id} and
                mainapp_detailshoe.size = {shoe_size} and
                mainapp_color.id = {color_id};
        '''

        shoes, detail_shoes, colors = SqlUtils.get_result(query, Shoe, DetailShoe, Color)

        if len(detail_shoes) == 0:
            err_code = ErrorCode.ERR_IN_ACT_SHOW_FINAL_CHOICE
            err_message = f'Xin lỗi {prefix_name}{customer_name}, hệ thống đã xảy ra lỗi. error code={err_code}'
            dispatcher.utter_message(text=err_message)
            return []
        elif detail_shoes[0].quantityAvailable < 1:
            text = 'Xin lỗi {}, đôi {} size {} màu {} hết hàng rồi ạ' \
                .format(prefix_name, shoe_model, shoe_size, color_name)
            dispatcher.utter_message(text=text)
            return []
        else:
            text = '{} thêm món này vào giỏ hàng giúp {} nhé'.format(bot_position, prefix_name)
            dispatcher.utter_message(text=text)

            horizontal_template_elements = []
            for index in range(len(shoes)):
                shoe = shoes[index]
                detail_shoe = detail_shoes[index]
                detail_shoe: DetailShoe

                buttons = [
                    PostBackButton(
                        title='Thêm vào giỏ hàng' + shoe.shoeModel,
                        str_send_to_webhook='thêm vào giỏ hàng'
                    ),
                    UrlButton(
                        title='Mua luôn đôi này',
                        url_access=MyWebUrl.get_detail_shoe_url(shoe.shoe_id)
                    ),
                ]

                element = HorizontalTemplateElement(
                    image_url=MyWebUrl.get_shoe_image_url(shoe.shoeThumbnail),
                    # image_url='https://www.w3schools.com/w3css/img_lights.jpg',
                    title=shoe.shoeName,
                    subtitle=f'màu: {color_name}, size: {shoe_size}\n ' + price_format(detail_shoe.newPrice),
                    default_action=HorizontalTemplateElement.DefaultAction(MyWebUrl.get_detail_shoe_url(shoe.shoe_id)),
                    list_buttons=buttons,
                )
                horizontal_template_elements.append(element)
            horizontal_template = HorizontalTemplate(horizontal_template_elements)
            dispatcher.utter_message(json_message=horizontal_template.to_json_message())

            # xem tiep
            quick_reply_elements = [
                QuickReplyElement(QuickReplyElement.TEXT, 'Xem giỏ hàng', 'cho xem giỏ hàng'),
                QuickReplyElement(QuickReplyElement.TEXT, 'Xem lại menu', 'tôi muốn xem menu'),
            ]
            quick_replies = QuickReplies(text_before_template='Tùy chọn khác',
                                         list_quick_reply_elements=quick_reply_elements)
            dispatcher.utter_message(json_message=quick_replies.to_json_message())

            # print('*****************************************************')
            # print(horizontal_template.to_json_message())
            # print('*****************************************************')
            # pprint(quick_replies.to_json_message())
        return []
