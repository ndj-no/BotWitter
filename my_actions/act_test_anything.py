from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from my_fb_api.button import UrlButton
from my_fb_api.button_template import ButtonTemplate
from my_fb_api.horizontal_template import HorizontalTemplate, HorizontalTemplateElement


class ActionTestAnything(Action):
    def name(self) -> Text:
        return 'act_test_anything'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = []
        elements = []
        buttons.extend([
            UrlButton('webview compact', 'https://9088ec6b.ngrok.io/account/contact_info/1234567/', UrlButton.COMPACT),
            UrlButton('webview tall', 'https://9088ec6b.ngrok.io/account/contact_info/1234567/', UrlButton.TALL),
            UrlButton('webview full', 'https://9088ec6b.ngrok.io/account/contact_info/1234567/', UrlButton.FULL),
        ])
        elements.extend([
            HorizontalTemplateElement(
                image_url='https://www.w3schools.com/w3css/img_lights.jpg',
                title='Generic template', subtitle='subtitle',
                default_action=HorizontalTemplateElement.DefaultAction(
                    'https://9088ec6b.ngrok.io/account/contact_info/1234567/'),
                list_buttons=buttons
            )
        ])
        template = HorizontalTemplate(elements)
        a = {"messages": [{"attachment": {"type": "template",
                                          "payload": {"template_type": "generic", "image_aspect_ratio": "square",
                                                      "elements": [
                                                          {"title": "Welcome!", "subtitle": "Choose your preferences",
                                                           "buttons": [{"type": "web_url",
                                                                        "url": "https://discreet-attic.glitch.me/show-webview",
                                                                        "title": "Webview (compact)",
                                                                        # "messenger_extensions": True,
                                                                        "webview_height_ratio": "compact"},
                                                                       {"type": "web_url",
                                                                        "url": "https://discreet-attic.glitch.me/show-webview",
                                                                        "title": "Webview (tall)",
                                                                        # "messenger_extensions": True,
                                                                        "webview_height_ratio": "tall"},
                                                                       {"type": "web_url",
                                                                        "url": "https://discreet-attic.glitch.me/show-webview",
                                                                        "title": "Webview (full)",
                                                                        # "messenger_extensions": True,
                                                                        "webview_height_ratio": "full"}]}]}}}]}
        dispatcher.utter_message(json_message=template.to_json_message())

        # print(template.to_json_message())
        print(a)
        return []
