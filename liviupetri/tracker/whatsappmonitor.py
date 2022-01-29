from liviupetri.whatsapp.client import WhatsappClient
from liviupetri.whatsapp.helpers.browsers import Browsers
from liviupetri.tracker.whatsappevent import WhatsAppEvent

import time


def whatsappmonitor(target):
    client = WhatsappClient(Browsers.CHROME, r"/Users/liviuhpetri/Library/Application Support/Google/Chrome/Profile 1")
    client.connect()

    event = WhatsAppEvent()

    while True:
        try:
            connected = client.is_logged()

            if connected:
                if target is None:
                    target = input('enter user name:')

                status = client.get_user_status(target)
                event.process_event(status)

        except Exception as e:
            print(e)

        time.sleep(1)


