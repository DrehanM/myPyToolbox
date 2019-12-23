import unittest
import codecaser
import os
import filecmp

class TestCasingFunctions(unittest.TestCase):

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


class TestCodecaser(unittest.TestCase):

    def test_small_file_camel_to_snake(self):
        self.maxDiff = None
        cc = codecaser.Codecaser('test_files/file1_camel.txt')
        cc.process(codecaser.camel_to_snake)

        with open(cc.output_path, 'r') as output_file, open('test_files/file1_snake.txt', 'r') as expected_file:
            output = output_file.read()
            expected = expected_file.read()
            try:
                self.assertMultiLineEqual(output, expected)
            finally:
                os.remove(cc.output_path)




if __name__ == '__main__':
    unittest.main()
