from selenium import webdriver

CHECKIN_URL = "https://www.southwest.com/air/check-in/index.html"

FIRST_NAME_ELEMENT_ID = "passengerFirstName"
LAST_NAME_ELEMENT_ID = "passengerLastName"
CONF_NUM_ELEMENT_ID = "confirmationNumber"
SUBMIT_ELEMENT_ID = "form-mixin--submit-button"

CONFIRM_CHECKIN_ELEMENT_CLASS = "air-checkin-review-results--check-in-button"
TEXT_TICKET_ELEMENT_CLASS = "boarding-pass-options--button-text"
PHONE_INPUT_ELEMENT_ID = "textBoardingPass"
PHONE_CONFIRMATION_ELEMENT_ID = "textBoardingPassConfirmation"


class Reservation:
    def __init__(self, first, last, conf_number, phone_number=None):
        self.first_name = first
        self.last_name = last
        self.confirmation_number = conf_number
        self.phone_number = phone_number

        self.driver = webdriver.Chrome()
        self.driver.get(CHECKIN_URL)

    def checkin(self):
        first_name_input = self.driver.find_element_by_id(FIRST_NAME_ELEMENT_ID)
        last_name_input = self.driver.find_element_by_id(LAST_NAME_ELEMENT_ID)
        confirmation_number_input = self.driver.find_element_by_id(CONF_NUM_ELEMENT_ID)
        checkin_button = self.driver.find_element_by_id(SUBMIT_ELEMENT_ID)

        first_name_input.send_keys(self.first_name)
        last_name_input.send_keys(self.last_name)
        confirmation_number_input.send_keys(self.confirmation_number)
        checkin_button.click()

    def confirm_reservation(self):
        confirm_button = self.driver.find_element_by_class_name(CONFIRM_CHECKIN_ELEMENT_CLASS)
        confirm_button.click()

    def text_boarding_pass(self):
        text_option_button = self.driver.find_element_by_class_name(TEXT_TICKET_ELEMENT_CLASS)
        text_option_button.click()

        phone_input = self.driver.find_element_by_id(PHONE_INPUT_ELEMENT_ID)
        phone_conf_input = self.driver.find_element_by_id(PHONE_CONFIRMATION_ELEMENT_ID)

        phone_input.send_keys(self.phone_number)
        phone_conf_input.send_keys(self.phone_number)

        confirm_phone_button = self.driver.find_element_by_id(SUBMIT_ELEMENT_ID)
        confirm_phone_button.click()











