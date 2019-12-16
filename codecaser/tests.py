import unittest
import codecaser
import os


class CodecaserTest(unittest.TestCase):

    def test_camel_to_snake(self):
        test_words = {
            "camelCase": "camel_case",
            "HTTPRequest": "http_request",
            "class.functionNameIsCamelCase(argumentOne)": "class.function_name_is_camel_case(argument_one)",
            "yOuCaNtCoNvErTtHiS": "y_ou_ca_nt_co_nv_er_tt_hi_s",
            "snake_case": "snake_case",
        }

        for test_word, answer in test_words.items():
            self.assertEqual(codecaser.camel_to_snake(test_word), answer)

    def test_snake_to_camel(self):
        pass


if __name__ == '__main__':
    unittest.main()
