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


def get_result(query: Text, class_type) -> List:
    out = []
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Thực thi sql và truyền 1 tham số.
        cursor.execute(query)
        for row in cursor:
            item = class_type(row)
            out.append(item)
    finally:
        # Đóng kết nối
        conn.close()
    return out
