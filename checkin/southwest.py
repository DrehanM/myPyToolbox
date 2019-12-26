from selenium import webdriver
import argparse
import pause
from datetime import datetime, timedelta
import os

CHECKIN_URL = "https://www.southwest.com/air/check-in/index.html"
MAX_ATTEMPTS = 3

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "bin/chromedriver")

FIRST_NAME_ELEMENT_ID = "passengerFirstName"
LAST_NAME_ELEMENT_ID = "passengerLastName"
CONF_NUM_ELEMENT_ID = "confirmationNumber"
SUBMIT_ELEMENT_ID = "form-mixin--submit-button"

CONFIRM_CHECKIN_ELEMENT_CLASS = "air-checkin-review-results--check-in-button"
TEXT_TICKET_ELEMENT_CLASS = "boarding-pass-options--button-text"
PHONE_INPUT_ELEMENT_ID = "textBoardingPass"
PHONE_CONFIRMATION_ELEMENT_ID = "textBoardingPassConfirmation"


class Reservation:
    def __init__(self, first, last, conf_number, flight_date, flight_time, phone_number=None):
        self.first_name = first
        self.last_name = last
        self.confirmation_number = conf_number
        self.phone_number = phone_number

        self.flight_date = flight_date
        self.flight_time = flight_time

        print(self.flight_date, self.flight_time)

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(executable_path=DRIVER_BIN, options=options)

    def checkin(self):
        self.driver.get(CHECKIN_URL)
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

        phone_input.clear()
        phone_conf_input.clear()

        phone_input.send_keys(self.phone_number)
        phone_conf_input.send_keys(self.phone_number)

        confirm_phone_button = self.driver.find_element_by_id(SUBMIT_ELEMENT_ID)
        confirm_phone_button.click()

    def sleep(self):
        checkin_time = self.get_checkin_time()
        pause.until(checkin_time)

    def get_checkin_time(self):
        date_map = {unit: int(d) for unit, d in zip(['month', 'day', 'year'], self.flight_date.split('-'))}
        time_map = {unit: int(t) for unit, t in zip(['hour', 'min'], self.flight_time.split(':'))}

        takeoff_datetime = datetime(date_map["year"], date_map["month"], date_map["day"], time_map["hour"],
                                    time_map["min"])
        checkin_datetime = takeoff_datetime - timedelta(days=1)

        return checkin_datetime

    def restart_driver(self):
        self.driver.close()
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(executable_path=DRIVER_BIN, options=options)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto checkin to Southwest flights.")
    parser.add_argument("first")
    parser.add_argument("last")
    parser.add_argument("conf_number")
    parser.add_argument("flight_date")
    parser.add_argument("flight_time")
    parser.add_argument("phone_number")

    args = parser.parse_args()

    r = Reservation(first=args.first, last=args.last, conf_number=args.conf_number, flight_date=args.flight_date,
                    flight_time=args.flight_time, phone_number=args.phone_number)

    r.sleep()

    for i in range(MAX_ATTEMPTS):
        try:
            r.checkin()
            r.confirm_reservation()
            r.text_boarding_pass()
        except:
            r.restart_driver()













