from typing import Text

from my_utils import SqlUtils
from my_utils.entitie_name import Entities
from my_utils.text_vi import remove_accents


class Category:
    TABLE_NAME = 'mainapp_category'
    COL_ID = 'category_id'
    COL_CATEGORY_NAME = 'categoryName'
    COL_DESCRIPTION = 'categoryDesc'

    def __init__(self, data):
        self.category_id = None
        self.categoryName = None
        self.categoryThumbnail = None
        self.categoryDesc = None
        self.__dict__.update(data)

    @staticmethod
    def get_id_by_name(category_name: Text):
        name2id = get_mapping_category2id()
        category_id = name2id.get(remove_accents(category_name.strip()))

        # neu co trong mapping thi return
        if category_id is not None:
            return category_id

        # else split and return if not None
        for text in remove_accents(category_name.strip()).split():
            category_id = name2id.get(text)
            if category_id is not None:
                return category_id

        # None if nothing in
        return None

    @staticmethod
    def get_query_where(att: Text, value: Text):
        """
        Neu att va value hop le thi tra ve query so sanh
        k thi tra ve empty string
        :param att:
        :param value:
        :return: String
        """
        where = {
            Entities.shoe_category: f'{Category.TABLE_NAME}.{Category.COL_ID} = ',
        }
        k = where.get(att)
        v = Category.get_id_by_name(value)
        if k is not None and v is not None:
            return k + str(v)
        return ''

    def __str__(self):
        return 'Category( id:{}_ name:{}_ thumbnail:{}_ description:{} )'.format(self.category_id, self.categoryName,
                                                                                 self.categoryThumbnail,
                                                                                 self.categoryDesc)


def get_mapping_category2id() -> dict:
    """
    :return: dict of types of shoes
    """
    da = 1
    luoi = 2
    the_thao = 3
    cao_co = 4
    vai = 5
    bata = 6

    mapping_category = {
        'leather': da,
        'da': da,
        'dà': da,
        'dả': da,
        'dá': da,
        'dạ': da,
        'dã': da,
        'gia': da,
        'ja': da,
        'ra': da,
        'lười': luoi,
        'luoi': luoi,
        'lườj': luoi,
        'luoj': luoi,
        'lazy': luoi,
        'lây dy': luoi,
        'lêy dy': luoi,
        'ley dy': luoi,
        'sport shoe': the_thao,
        'thể thao': the_thao,
        'the thao': the_thao,
        'thethao': the_thao,
        'thểthao': the_thao,
        'sneaker': the_thao,
        'sneakers': the_thao,
        'cao cổ': cao_co,
        'cao cỏ': cao_co,
        'caocỏ': cao_co,
        'caocổ': cao_co,
        'cao co': cao_co,
        'caoco': cao_co,
        'kao cổ': cao_co,
        'kout cổ': cao_co,
        'cout cổ': cao_co,
        'vải': vai,
        'vài': vai,
        'vái': vai,
        'vãi': vai,
        'vại': vai,
        'vai': vai,
        'pata': bata,
        'bata': bata,
        'bât': bata,
        'ba ta': bata,
        'bâta': bata,
        'bâtâ': bata,
        'bâ ta': bata,
        'beta': bata,
        '3ta': bata,
        '3 ta': bata,
    }

    query = f'select id as category_id, categoryName from {Category.TABLE_NAME}'
    categories = SqlUtils.get_result(query, Category)
    dict_categories = dict()
    for category in categories:
        dict_categories[remove_accents(category.categoryName).lower()] = category.category_id
    mapping_category.update(dict_categories)

    return mapping_category
