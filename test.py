import time

a = {
    'attachment': {''
                   'type': 'template',
                   'payload': {
                       'template_type': 'receipt',
                       'recipient_name': 'Nguyễn Đình Giang',
                       'order_number': '10',
                       'currency': 'VND',
                       'payment_method': 'Thanh toán khi nhận hàng',
                       'order_url': 'https://b534c540.ngrok.io/order/detail/10/',
                       'timestamp': '1589216400',
                       'address': {
                           'street_1': '098 765 4321',
                           'street_2': 'DHCN Hà Nội',
                           'city': '_',
                           'postal_code': '_',
                           'state': '_',
                           'country': 'VN'
                       },
                       'summary': {
                           'subtotal': 1900000,
                           'shipping_cost': 0,
                           'total_tax': 0,
                           'total_cost': 1615000
                       },
                       'adjustments': [
                           {
                               'name': 'Mã giảm giá 15%',
                               'amount': 285000
                           }
                       ],
                       'elements': [
                           {
                               'title': 'Giày lười Louis Vuitton họa tiết da nhăn GLLV25',
                               'subtitle': 'màu: Đen, size: 44',
                               'quantity': 3,
                               'price': None,
                               'currency': 'VND',
                               'image_url': 'https://dictionary.cambridge.org/vi/images/thumb/Tshirt_noun_001_18267.jpg'
                           },
                           {
                               'title': 'Giày thể thao B771',
                               'subtitle': 'màu: Đen, size: 41',
                               'quantity': 1,
                               'price': None,
                               'currency': 'VND',
                               'image_url': 'https://dictionary.cambridge.org/vi/images/thumb/Tshirt_noun_001_18267.jpg'}]}}}

message = {
    "attachment": {
        "type": "template",
        "payload": {
            "template_type": "receipt",
            "recipient_name": "Stephane Crozatier",
            "order_number": "chưa đặt",
            "currency": "VND",
            "payment_method": "Visa 2345",
            "order_url": "http://petersapparel.parseapp.com/order?order_id=123456",
            "timestamp": str(time.time()).split('.')[0],
            "address": {
                "street_1": "1 Hacker Way",
                "street_2": "",
                "city": "_",
                "postal_code": "_",
                "state": "_",
                "country": "VN"
            },
            "summary": {
                "subtotal": 7500000,
                "shipping_cost": 0,
                "total_tax": 0,
                "total_cost": 560000
            },
            "adjustments": [
                {
                    "name": "New Customer Discount",
                    "amount": 20
                },
                {
                    "name": "$10 Off Coupon",
                    "amount": 10
                }
            ],
            "elements": [
                {
                    "title": "Classic White T-Shirt",
                    "subtitle": "100% Soft and Luxurious Cotton",
                    "quantity": 2,
                    "price": 50,
                    "currency": "VND",
                    "image_url": "https://dictionary.cambridge.org/vi/images/thumb/Tshirt_noun_001_18267.jpg"
                },
                {
                    "title": "Classic Gray T-Shirt",
                    "subtitle": "100% Soft and Luxurious Cotton",
                    "quantity": 1,
                    "price": 250000,
                    "currency": "VND",
                    "image_url": "https://dictionary.cambridge.org/vi/images/thumb/Tshirt_noun_001_18267.jpg"
                }
            ]
        }
    }
}
