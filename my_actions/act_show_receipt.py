from typing import Dict, List, Text, Any

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_models.order_package import OrderPackage
# from my_utils.table_name import Tables
from my_utils.SqlUtils import get_result
from my_models.user import User


class ActionShowReceipt(Action):
    """
    get a list of categories
    """

    def name(self) -> Text:
        return "act_show_receipt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.current_state()['sender_id']

        query = f'SELECT * ' \
                f'FROM {OrderPackage.TABLE_NAME} INNER JOIN {OrderPackage.TABLE_NAME} ' \
                f'on ( {User.TABLE_NAME}.id = {OrderPackage.TABLE_NAME}.user_id ) ' \
                f'WHERE {User.TABLE_NAME}.id = {user_id} order by '
        get_result(query, OrderPackage)
        message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "receipt",
                    "recipient_name": "Stephane Crozatier",
                    "order_number": "12345678902",
                    "currency": "USD",
                    "payment_method": "Visa 2345",
                    "order_url": "http://petersapparel.parseapp.com/order?order_id=123456",
                    "timestamp": "1428444852",
                    "address": {
                        "street_1": "1 Hacker Way",
                        "street_2": "",
                        "city": "Menlo Park",
                        "postal_code": "94025",
                        "state": "CA",
                        "country": "US"
                    },
                    "summary": {
                        "subtotal": 75.00,
                        "shipping_cost": 4.95,
                        "total_tax": 6.19,
                        "total_cost": 56.14
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
                            "currency": "USD",
                            "image_url": "https://dictionary.cambridge.org/vi/images/thumb/Tshirt_noun_001_18267.jpg"
                        },
                        {
                            "title": "Classic Gray T-Shirt",
                            "subtitle": "100% Soft and Luxurious Cotton",
                            "quantity": 1,
                            "price": 25,
                            "currency": "USD",
                            "image_url": "https://dictionary.cambridge.org/vi/images/thumb/Tshirt_noun_001_18267.jpg"
                        }
                    ]
                }
            }
        }
        user_id = (tracker.current_state())["sender_id"]
        dispatcher.utter_message(text=str(user_id), json_message=message)
        return []
