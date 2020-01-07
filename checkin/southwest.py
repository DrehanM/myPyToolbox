from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import argparse
import pause
from datetime import datetime, timedelta
import os
import logging

CHECKIN_URL = "https://www.southwest.com/air/check-in/index.html"
MAX_ATTEMPTS = 3

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "bin/chromedriver")

FIRST_NAME_ELEMENT_ID = "passengerFirstName"
LAST_NAME_ELEMENT_ID = "passengerLastName"
CONF_NUM_ELEMENT_ID = "confirmationNumber"
SUBMIT_ELEMENT_ID = "form-mixin--submit-button"

CONFIRM_CHECKIN_ELEMENT_CLASS = "submit-button"
TEXT_TICKET_ELEMENT_CLASS = "boarding-pass-options--button-text"
PHONE_INPUT_ELEMENT_ID = "textBoardingPass"
PHONE_CONFIRMATION_ELEMENT_ID = "textBoardingPassConfirmation"

LOGGING_FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=LOGGING_FORMAT)
LOGGER = logging.getLogger("southwest-checkin-script")


class Reservation:
    def __init__(self, first, last, conf_number, flight_date, flight_time, phone_number=None):
        self.first_name = first
        self.last_name = last
        self.confirmation_number = conf_number
        self.phone_number = phone_number

        self.flight_date = flight_date
        self.flight_time = flight_time

        LOGGER.critical("Set up auto check-in for {first} {last} with confirmation number {conf}"
                        .format(first=first, last=last, conf=conf_number))

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
        pause.sleep(3)
        confirm_button = self.driver.find_element_by_class_name(CONFIRM_CHECKIN_ELEMENT_CLASS)
        pause.sleep(1)
        LOGGER.critical("Confirming Reservation...")
        confirm_button.click()

    def text_boarding_pass(self):
        pause.sleep(1)
        try:
            text_option_button = self.driver.find_element_by_class_name(TEXT_TICKET_ELEMENT_CLASS)
        except NoSuchElementException:
            LOGGER.error("Cannot text boarding pass. Reservation is either international or for multiple passengers.")
            return

        pause.sleep(1)
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
        LOGGER.critical("Going to sleep until {time}".format(time=checkin_time))
        pause.until(checkin_time)

    def get_checkin_time(self):
        date_map = {unit: int(d) for unit, d in zip(['month', 'day', 'year'], self.flight_date.split('-'))}
        time_map = {unit: int(t) for unit, t in zip(['hour', 'min'], self.flight_time.split(':'))}

        takeoff_datetime = datetime(date_map["year"], date_map["month"], date_map["day"], time_map["hour"],
                                    time_map["min"])
        checkin_datetime = takeoff_datetime - timedelta(days=1) + timedelta(seconds=10)

        return checkin_datetime

    def start_driver(self):
        LOGGER.critical("Starting Chrome Driver...")
        options = webdriver.ChromeOptions()
        options.headless = False
        self.driver = webdriver.Chrome(executable_path=DRIVER_BIN, options=options)
        self.driver.implicitly_wait(3)

    def kill_driver(self):
        LOGGER.critical("Killing Chrome Driver and exiting script...")
        self.driver.close()

    def restart_driver(self):
        self.kill_driver()
        self.start_driver()


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

    r.start_driver()

    for i in range(MAX_ATTEMPTS):
        try:
            r.checkin()
            r.confirm_reservation()
            break
        except Exception as e:
            LOGGER.exception("Exception occurred, restarting...")
            r.restart_driver()

    r.text_boarding_pass()

    r.kill_driver()













