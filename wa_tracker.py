from liviupetri.whatsapp.helpers.browsers import Browsers
from liviupetri.whatsapp.client import WhatsappClient
from liviupetri.user.user import User

client = WhatsappClient(Browsers.CHROME, r"/Users/liviuhpetri/Library/Application Support/Google/Chrome/Profile 1")

if not client.connect():
    exit('Not connected! Check your internet connection! ERR: 901')

user = None
user_name = 'Liviu RO'

if client.is_logged():
    user = User(user_name, client)
else:
    print("WhatsApp log-in failure! Check your credentials! - ERR: 902")

while True:
    try:
        if client.is_logged() and user is None:
            pass
    except False:
        pass
