from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.horizontal_template import HorizontalTemplate
from my_models.category import Category
from my_models.detail_shoe import DetailShoe
from my_models.shoe import Shoe
from my_utils import SqlUtils
from my_utils.debug import debug
from my_utils.entitie_name import Entities


class ActionShowShoesByCategory(Action):

    def name(self) -> Text:
        return "act_show_shoes_by_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        prefix_name = tracker.get_slot(Entities.prefix_name)
        customer_name = tracker.get_slot(Entities.customer_name)
        bot_position = tracker.get_slot(Entities.bot_position)
        shoe_category = tracker.get_slot(Entities.shoe_category)

        debug('\n_________action_show_shoes_by_category_________')
        debug('category ', shoe_category)

        if shoe_category is None or shoe_category.strip() == '':
            dispatcher.utter_message(text=f'Xin lỗi {prefix_name} chưa cung cấp tên loại giày muốn tìm.')
            return []

        category_id = Category.get_id_by_name(shoe_category)
        debug('category_id ', category_id)

        if not category_id:
            message_not_found = 'Xin lỗi ' + prefix_name + customer_name \
                                + '. Hiện bên ' + bot_position + ' không kinh doanh mặt hàng này ạ'
            dispatcher.utter_message(text=message_not_found)
            return []
        query = f'''
            select distinct 
                mainapp_shoe.id as shoe_id, 
                mainapp_shoe.shoeName,
                mainapp_shoe.shoeModel,
                mainapp_shoe.shoeThumbnail,
                mainapp_category.categoryName,
                mainapp_detailshoe.id as detailShoe_id,
                min(mainapp_detailshoe.newPrice) as newPrice,
                sum(mainapp_detailshoe.quantityAvailable) as totalQuantityAvailable
            from mainapp_shoe 
                inner join mainapp_detailshoe 
                    on mainapp_shoe.id = mainapp_detailshoe.shoe_id
                inner join mainapp_category
                    on mainapp_shoe.category_id = mainapp_category.id
            where 
                active = 1 and
                mainapp_category.id = {category_id}
            group by 
                mainapp_shoe.id, 
                mainapp_shoe.shoeName,
                mainapp_shoe.shoeModel,
                mainapp_shoe.shoeThumbnail,
                mainapp_category.categoryName,
                mainapp_detailshoe.id
            having
                totalQuantityAvailable > 0
            limit 0, 5;    
        '''
        shoes, detail_shoes = SqlUtils.get_result(query, Shoe, DetailShoe)

        if len(shoes) == 0:
            message = 'Xin lỗi ' + prefix_name + customer_name \
                      + '. Hiện ' + bot_position + ' không tìm thấy đôi giày ' + shoe_category + ' nào ạ'
            dispatcher.utter_message(message)
        else:
            horizontal_template = HorizontalTemplate.from_shoes_shoe_detail_shoe(shoes=shoes, detail_shoes=detail_shoes)
            dispatcher.utter_message(json_message=horizontal_template.to_json_message())

        debug('query', query)
        debug('tìm thấy ' + str(len(shoes)) + ' KQ')

        return []
