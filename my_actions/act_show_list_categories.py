from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.quick_replies_template import QuickReplyElement, QuickReplies
from my_models.category import Category
from my_utils import SqlUtils
from my_utils.debug import debug
from my_utils.entitie_name import Entities


class ActionShowListCategory(Action):
    """
    get a list of categories
    """

    def name(self) -> Text:
        return "act_show_list_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('_____' + self.name())


        prefix_name = tracker.get_slot(Entities.customer_name)
        customer_name = tracker.get_slot(Entities.customer_name)
        bot_position = tracker.get_slot(Entities.bot_position)

        query = f'SELECT * FROM {Category.TABLE_NAME}'
        categories = SqlUtils.get_result(query, Category)
        if len(categories) == 0:
            message = 'Xin lỗi ' + prefix_name + customer_name + '. ' \
                      + bot_position + ' không tìm thấy category nào trong cơ sở dữ liệu.'
            dispatcher.utter_message(message)
        else:
            quick_reply_elements = []
            for category in categories:
                element = QuickReplyElement(
                    content_type=QuickReplyElement.TEXT,
                    title=category.categoryName,
                    payload=f'cho a xem loại giày {category.categoryName}'
                )
                quick_reply_elements.append(element)
            quick_reply_template = QuickReplies(
                text_before_template=f'Hiện bên {bot_position} có những loại này. Mời {prefix_name} chọn:',
                list_quick_reply_elements=quick_reply_elements
            )
            dispatcher.utter_message(json_message=quick_reply_template.to_json_message())
        return []
