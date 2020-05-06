from typing import Text

from my_models import mapping_att
from my_utils.entitie_name import Entities
from my_utils.text_vi import no_accent


class Category:
    TABLE_NAME = 'mainapp_category'
    COL_ID = 'category_id'
    COL_CATEGORY_NAME = 'categoryName'
    COL_DESCRIPTION = 'categoryDesc'

    def __init__(self, data):
        self.category_id = -1
        self.categoryName = None
        self.categoryThumbnail = None
        self.categoryDesc = None
        self.__dict__.update(data)

    @staticmethod
    def get_type_by_name(category_name: Text):
        name2id = mapping_att.get_mapping_category2id()
        category_type = name2id.get(no_accent(category_name.strip()))

        # neu co trong mapping thi return
        if category_type is not None:
            return category_type

        # else split and return if not None
        for text in no_accent(category_name.strip()).split():
            category_type = name2id.get(text)
            if category_type is not None:
                return category_type

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
        v = Category.get_type_by_name(value)
        if k is not None and v is not None:
            return k + str(v)
        return ''

    def __str__(self):
        return 'Category( id:{}_ name:{}_ thumbnail:{}_ description:{} )'.format(self.id, self.categoryName,
                                                                                 self.categoryThumbnail,
                                                                                 self.categoryDesc)
