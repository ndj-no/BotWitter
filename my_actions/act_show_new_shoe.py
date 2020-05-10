from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.HorizontalTemplate import HorizontalTemplateElement, HorizontalTemplate
from my_fb_api.QuickRepliesTemplate import QuickReplyElement, QuickReplies
from my_fb_api.button import PostBackButton, UrlButton
from my_models.detail_shoe import DetailShoe
from my_models.shoe import Shoe
from my_utils import SqlUtils
from my_utils.entitie_name import Entities
from my_utils.error_code import ErrorCode
from my_utils.price_format import price_format
from my_web_setting.my_web_url import MyWebUrl


class ActionShowNewShoe(Action):
    def name(self) -> Text:
        return 'act_show_new_shoe'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Trả về generic template 6 sản phẩm hot + quick replies đòi xem thêm

        :param dispatcher:
        :param tracker:
        :param domain:
        :return:
        """
        # debug('\n_________act_shoe_new_shoe_________')

        prefix_name = tracker.get_slot(Entities.prefix_name)
        customer_name = tracker.get_slot(Entities.customer_name)
        bot_position = tracker.get_slot(Entities.bot_position)

        query = 'SELECT * FROM NEW_SHOES'
        shoes = SqlUtils.get_result(query, Shoe)
        detail_shoes = SqlUtils.get_result(query, DetailShoe)
        if len(detail_shoes) == 0 or len(shoes) == 0:
            err_code = ErrorCode.ERR_IN_ACT_GET_NEW_SHOE
            err_message = f'Xin lỗi {prefix_name}{customer_name}, hệ thống đã xảy ra lỗi. error code={err_code}'
            dispatcher.utter_message(text=err_message)
        else:
            dispatcher.utter_message(
                text='Đây là 5 đôi bên ' + bot_position + ' mới nhập đó ' + prefix_name + customer_name)
            # horizontal_template_elements = []
            # for index in range(len(shoes)):
            #     shoe = shoes[index]
            #     detail_shoe = detail_shoes[index]
            #
            #     buttons = [
            #         PostBackButton(
            #             title='Xem đôi này ' + shoe.shoeModel,
            #             str_send_to_webhook='tôi muốn xem mẫu ' + shoe.shoeModel + ' id ' + str(shoe.shoe_id)
            #         ),
            #         UrlButton(
            #             title='Xem trên website',
            #             url_access=MyWebUrl.get_detail_shoe_url(shoe.shoe_id)
            #         ),
            #     ]
            #
            #     element = HorizontalTemplateElement(
            #         image_url=MyWebUrl.get_shoe_image_url(shoe.shoeThumbnail),
            #         # image_url='https://www.w3schools.com/w3css/img_lights.jpg',
            #         title=shoe.shoeName,
            #         subtitle=price_format(detail_shoe.newPrice),
            #         default_action=HorizontalTemplateElement.DefaultAction(MyWebUrl.get_detail_shoe_url(shoe.shoe_id)),
            #         list_buttons=buttons,
            #     )
            #     horizontal_template_elements.append(element)
            # horizontal_template = HorizontalTemplate(horizontal_template_elements)

            horizontal_template = HorizontalTemplate.from_shoes_shoe_detail_shoe(shoes=shoes, detail_shoes=detail_shoes)
            dispatcher.utter_message(json_message=horizontal_template.to_json_message())

            # xem tiep
            quick_reply_elements = [
                QuickReplyElement(QuickReplyElement.TEXT, 'Xem thêm', 'còn đôi nào khác k?'),
                QuickReplyElement(QuickReplyElement.TEXT, 'Xem lại menu', 'tôi muốn xem menu'),
            ]
            quick_replies = QuickReplies(text_before_template='Tùy chọn khác',
                                         list_quick_reply_elements=quick_reply_elements)
            dispatcher.utter_message(json_message=quick_replies.to_json_message())
        return []
