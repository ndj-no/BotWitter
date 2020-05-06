from typing import Text
from my_models import mapping_att
from my_utils.entitie_name import Entities


class Color:
    TABLE_NAME = 'mainapp_color'
    COL_COLOR_NAME = 'colorName'
    COL_COLOR_DESC = 'colorDesc'

    def __init__(self, data):
        self.color_id = -1
        self.colorName = None
        self.colorDesc = None
        self.__dict__.update(data)

    @staticmethod
    def get_id_by_color_name(color_name: Text):
        name2type = mapping_att.get_mapping_color2id()
        color_type = name2type.get(color_name.strip())
        # neu co trong mapping thi return
        if color_type is not None:
            return color_type

        # else split and return
        for text in color_name.strip().split():
            color_type = name2type.get(text)
            if color_type is not None:
                return color_type

        # None if nothing in
        return None

    @staticmethod
    def get_query_where(att: Text, value: Text) -> Text:
        where = {
            Entities.shoe_color: f' {Color.TABLE_NAME}.id = ',
        }
        k = where.get(att)
        v = Color.get_id_by_color_name(value)
        if k is not None and v is not None:
            return k + str(v)
        else:
            return ''

    def __str__(self):
        return 'Color( id:{:<3}_ colorName:{:<10}_ colorDesc:{:<10} )'.format(self.id, self.colorName, self.colorDesc)
