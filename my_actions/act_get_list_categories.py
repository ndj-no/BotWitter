from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_models.category import Category
from my_utils import SqlUtils
from my_utils.debug import debug
from my_utils.entitie_name import Entities


class ActionGetListCategory(Action):
    """
    get a list of categories
    """

    def name(self) -> Text:
        return "act_get_list_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        debug('\n_________action_find_list_category_________')

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
            message = 'Tìm thấy ' + str(len(categories)) + ' KQ.'
            count = 1
            for category in categories:
                message += '\n' + str(count) + '.' + category.name
            dispatcher.utter_message(message)
        debug('query\n', query)
        debug('tìm thấy ' + str(len(categories)) + ' KQ')
        return []
