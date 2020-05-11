from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_models.category import Category
from my_models.shoe import Shoe
from my_utils import SqlUtils
from my_utils.debug import debug
from my_utils.entitie_name import Entities


class ActionShowShoesByCategory(Action):
    """
    get a list of categories
    """

    def name(self) -> Text:
        return "act_show_shoes_by_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        category = tracker.get_slot(Entities.shoe_category)

        debug('\n_________action_show_shoes_by_category_________')
        debug('category ', category)

        if category is None or category.strip() == '':
            dispatcher.utter_template('utter_not_provide_category', tracker)
        else:
            prefix_name = tracker.get_slot(Entities.prefix_name)
            customer_name = tracker.get_slot(Entities.customer_name)
            bot_position = tracker.get_slot(Entities.bot_position)

            query_where = Category.get_query_where(Entities.shoe_category, category)

            if query_where == '':
                message_not_found = 'Xin lỗi ' + prefix_name + customer_name \
                                    + '. Hiện bên ' + bot_position + ' không kinh doanh mặt hàng này ạ'
                dispatcher.utter_message(message_not_found)
            query = f'SELECT * ' \
                    f'FROM {Shoe.TABLE_NAME} INNER JOIN {Shoe.TABLE_NAME} ' \
                    f'ON ({Shoe.TABLE_NAME}.category_id = {Shoe.TABLE_NAME}.id) ' \
                    f'WHERE {query_where};'
            shoes = SqlUtils.get_result(query, Shoe)
            if len(shoes) == 0:
                message = 'Xin lỗi ' + prefix_name + customer_name \
                          + '. Hiện ' + bot_position + ' không tìm thấy đôi giày ' + category + ' nào ạ'
                dispatcher.utter_message(message)
            else:
                message = 'Tìm thấy ' + str(len(shoes)) + ' KQ.'
                count = 1
                for shoe in shoes:
                    message += '\n' + str(count) + '.' + shoe.name
                    count += 1
                dispatcher.utter_message(message)

            debug('query', query)
            debug('tìm thấy ' + str(len(shoes)) + ' KQ')

        return []
