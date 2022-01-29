from liviupetri.whatsapp.helpers.status import Status
from liviupetri.whatsapp.helpers.browsers import Browsers

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from PIL import Image
from io import BytesIO

import os.path
import time
import ast


class WhatsappClient:
    def __init__(self, browser: Browsers, profile_path: str = None):
        options = Options()

        if browser == Browsers.CHROME:
            if profile_path is not None:
                options.add_argument(r'user-data-dir={0}'.format(profile_path))

            self.__webdriver = webdriver.Chrome(chrome_options=options)

        self.__chat = None

        self.__enter_action = ActionChains(self.__webdriver)
        self.__enter_action.send_keys(Keys.ENTER)

        self.__esc_action = ActionChains(self.__webdriver)
        self.__esc_action.send_keys(Keys.ESCAPE)

        my_path = os.path.abspath(os.path.dirname(__file__))
        self.__path = os.path.join(my_path, "xpaths.cfg")

    def connect(self) -> bool:
        try:
            self.__webdriver.get("https://web.whatsapp.com")
            self.__wait = WebDriverWait(self.__webdriver, 5)
        except:
            print("Connection not possible. Check your internet connection!")
            return False
        return True

    def close(self) -> bool:
        try:
            self.__webdriver.quit()
        except:
            print("Couldn't close the connection...")
            return False
        print("Connection closed :)")
        return True

    def minimize_window(self):
        self.__webdriver.minimize_window()

    def maximize_window(self):
        self.__webdriver.maximize_window()

    def is_logged(self) -> bool:
        try:
            self.__webdriver.find_element(By.XPATH, self.__get_xpath("IS_LOGGED"))
        except:
            print("Could not find is logged element!", self.__get_xpath("IS_LOGGED"))
            return False
        return True

    def save_qrcode(self, filename: str) -> bool:
        im = self.__get_img_by_variable("QR_CODE")

        if im != None:
            im.save(filename)
            return True
        return False

    def save_header(self, filename: str) -> bool:
        im = self.__get_img_by_variable("HEADER")

        if im != None:
            im.save(filename)
            return True
        return False

    def get_header(self) -> bool:
        im = self.__get_img_by_variable("HEADER")

        if im == None:
            return None
        width, height = im.size
        im = im.crop((8, 8, width - width * 8.5, height))

        b = BytesIO()
        im.save(b, "PNG")
        b.seek(0)
        return b

    def open_chat(self, target: str) -> bool:
        if self.__chat == target.lower():
            return True

        try:
            new_chat_title = self.__wait.until(
                EC.presence_of_element_located((By.XPATH, self.__get_xpath("NEW_CHAT_BTN"))))
            new_chat_title.click()

            search_box = self.__wait.until(EC.presence_of_element_located((By.XPATH, self.__get_xpath("SEARCH_AREA"))))
            search_box.send_keys(target)

            time.sleep(1)

            try:
                chat_found = self.__wait.until(
                    EC.presence_of_element_located((By.XPATH, self.__get_xpath("CONTACT_LIST"))))

                self.__enter_action.perform()
                self.__chat = target.lower()

            except:
                self.__esc_action.perform()
                self.__esc_action.perform()
                print("Incorrect name, no chat found!")
                return False
        except Exception as e:
            print(e)
            return False
        return True

    def get_user_status(self, target: str) -> Status:
        if self.open_chat(target):
            try:
                status_element = self.__webdriver.find_element(By.XPATH, self.__get_xpath("USER_STATUS"))
                # profile_name_element = self.__webdriver.find_element(By.XPATH, self.__get_xpath("PROFILE_NAME"))

                # if profile_name_element.text.lower() != target:
                #     return Status.USER_CHANGED
                if Status.SETUP.value in status_element.text:
                    return Status.SETUP
                elif status_element.text == Status.ONLINE.value:
                    return Status.ONLINE
                elif Status.TYPING.value in status_element.text.lower():
                    return Status.TYPING
                elif Status.RECORDING.value in status_element.text.lower():
                    return Status.RECORDING
                elif Status.TYPING.value in status_element.text.lower():
                    return Status.TYPING
                elif Status.LAST_SEEN in status_element.text.lower():
                    return Status.LAST_SEEN
            except:
                return Status.OFFLINE
        return Status.NOT_DEFINED

    def send_message(self, target: str, message: str) -> bool:
        if not self.open_chat(target):
            return False

        try:
            self.__webdriver.switch_to.active_element.send_keys(message)
            self.__enter_action.perform()
        except:
            return False
        return True

    def __get_img_by_variable(self, variable_name: str) -> Image:
        try:
            element = self.__webdriver.find_element(By.XPATH, self.__get_xpath(variable_name))
            location = element.location
            size = element.size
            png = self.__webdriver.get_screenshot_as_png()

            im = Image.open(BytesIO(png))

            left = location['x']
            top = location['y']
            right = left + size['width']
            bottom = top + size['height']

            im = im.crop(left, top, right, bottom)
            return im
        except:
            return None

    def __get_xpath(self, variable_name: str) -> str:
        xpaths = ast.literal_eval(open(self.__path).read())
        return xpaths[variable_name]

