import unittest
import codecaser
import os


class TestCodecaser(unittest.TestCase):

    def file_diff(func):
        def f(self, *args, **kwargs):
            self.maxDiff = None
            cc_processed_instance, expected_filename = func(self, *args, **kwargs)
            with open(cc_processed_instance.output_path, 'r') as output_file, open(expected_filename, 'r') as exp_file:
                output = output_file.read()
                expected = exp_file.read()
                try:
                    self.assertMultiLineEqual(output, expected)
                finally:
                    os.remove(cc_processed_instance.output_path)
        return f

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
        test_words = {
            "camel_case": "camelCase",
            "http_request": "httpRequest",
            "class.function_name_is_camel_case(argument_one)": "class.functionNameIsCamelCase(argumentOne)",
            "y_ou_ca_nt_co_nv_er_tt_hi_s": "yOuCaNtCoNvErTtHiS",
            "snake_case": "snakeCase",
            "_ignores_strings_with_leading_underscore": "_ignores_strings_with_leading_underscore",
        }

        for test_word, answer in test_words.items():
            self.assertEqual(codecaser.snake_to_camel(test_word), answer)

    @file_diff
    def test_small_file_camel_to_snake(self):
        cc = codecaser.Codecaser(input_path='test_files/file1_camel.txt', in_place=False, output_filename=None)
        cc.process(codecaser.CASING_FUNCTIONS['camel']['snake'])
        expected_filename = 'test_files/file1_snake.txt'
        return cc, expected_filename

    @file_diff
    def test_small_file_snake_to_camel(self):
        cc = codecaser.Codecaser(input_path='test_files/file1_snake.txt', in_place=False, output_filename=None)
        cc.process(codecaser.CASING_FUNCTIONS['snake']['camel'])
        expected_filename = 'test_files/file1_camel.txt'
        return cc, expected_filename


if __name__ == '__main__':
    unittest.main()
