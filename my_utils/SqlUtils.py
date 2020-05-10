from typing import List, Text

import pymysql.cursors


def get_connection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='wittershoedb',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def get_result(query: Text, *class_types) -> List:
    out = [[] for _ in class_types]
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Thực thi sql và truyền 1 tham số.
        cursor.execute(query)
        for row in cursor:
            for index, class_type in enumerate(class_types):
                item = class_type(row)
                out[index].append(item)
    finally:
        # Đóng kết nối
        conn.close()

    if len(out) == 1:
        return out[0]
    else:
        return out
