from typing import Dict


def get_mapping_color2id() -> Dict:
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
    return dict_mapping_color


def get_mapping_category2id() -> Dict:
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
    return mapping_category
