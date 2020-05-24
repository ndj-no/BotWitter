from typing import Text
from my_utils import SqlUtils
from my_utils.entitie_name import Entities
from my_utils.text_vi import remove_accents


class Color:
    TABLE_NAME = 'mainapp_color'
    COL_COLOR_NAME = 'colorName'
    COL_COLOR_DESC = 'colorDesc'

    def __init__(self, data):
        self.color_id = None
        self.colorName = None
        self.colorDesc = None
        self.__dict__.update(data)

    @staticmethod
    def get_id_by_color_name(color_name: Text):
        color_name = remove_accents(color_name).lower()
        name2id = get_mapping_color2id()
        color_id = name2id.get(color_name.strip())
        # neu co trong mapping thi return
        if color_id is not None:
            return color_id

        # else split and return
        for text in color_name.strip().split():
            color_id = name2id.get(text)
            if color_id is not None:
                return color_id

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


def get_mapping_color2id() -> dict:
    black = 1
    white = 2
    red = 3
    yellow = 4
    brown = 5
    gray = 6
    blue = 7
    green = 8
    pink = 9
    colorful = 10

    dict_mapping_color = {
        'đen': black,
        'den': black,
        'black': black,
        'white': white,
        'trắng': white,
        'trang': white,
        'red': red,
        'đỏ': red,
        'do': red,
        'yellow': yellow,
        'yeallow': yellow,
        'yealow': yellow,
        'vàng': yellow,
        'vang': yellow,
        'brown': brown,
        'bron': brown,
        'brow': brown,
        'đất': brown,
        'nâu': brown,
        'nau': brown,
        'lau': brown,
        'lâu': brown,
        'gray': gray,
        'grey': gray,
        'xám': gray,
        'xam': gray,
        'gry': gray,
        'blue': blue,
        'blu': blue,
        'xanh': blue,
        'xanh lam': blue,
        'lam': blue,
        'xanh dương': blue,
        'xanh duong': blue,
        'xanh nước biển': blue,
        'xanh nuoc bien': blue,
        'dương': blue,
        'duong': blue,
        'nước biển': blue,
        'nước bien': blue,
        'nước': blue,
        'nuoc': blue,
        'nuoc bien': blue,
        'pink': pink,
        'pik': pink,
        'ping': pink,
        'hồng': pink,
        'hong': pink,
        'colorful': colorful,
        'corlorful': colorful,
        'coloful': colorful,
        'colorfull': colorful,
        'nhiều màu': colorful,
        'nhieu mau': colorful,
        'nhiều mau': colorful,
        'nhieu màu': colorful,
        'đa sắc': colorful,
        'da sac': colorful,
        'sặc sỡ': colorful,
        'sắc sặc sỡ': colorful,
        'sac sỡ': colorful,
        'sặc so': colorful,
        'sac so': colorful,
        'sặc xỡ': colorful,
        'xặc sỡ': colorful,
        'green': green,
        'gren': green,
        'lục': green,
        'luc': green,
        'xanh lá cây': green,
        'xanh la cay': green,
        'lá cây': green,
        'la cay': green,
        'lá': green,
        'la': green,
        'cây': green,
        'cay': green,
    }

    # update from database if any new color that haven't update this file yet
    query = f'select id as color_id, colorName from {Color.TABLE_NAME}'
    colors = SqlUtils.get_result(query, Color)
    dict_colors = dict()
    for color in colors:
        dict_colors[remove_accents(color.colorName).lower()] = color.color_id
    dict_mapping_color.update(dict_colors)

    return dict_mapping_color
