import argparse
import os
import re
import keyword
import builtins

# Precompiled Regex (for faster processing) #
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


# Casing Functions
# --##--##--##--##--##--##--##--##--##-- #
def camel_to_snake(string):
    s1 = first_cap_re.sub(r'\1_\2', string)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def snake_to_camel(string):
    pass


# --##--##--##--##--##--##--##--##--##-- #

# Casing Function Map (Nested mapped to from_case and to_case) #
CASING_FUNCTIONS = {
    'snake': {
        'camel': camel_to_snake
    },
    'camel': {
        'snake': snake_to_camel
    }
}


class Codecaser:
    def __init__(self, input_path, in_place=False, output_filename=None):
        self.input_path = input_path
        self.dir, self.input_filename = os.path.split(input_path)
        if in_place:
            self.output_path = os.path.join(self.dir, self.input_filename)
        else:
            if output_filename is not None:
                self.output_path = os.path.join(self.dir, output_filename)
            else:
                self.output_path = os.path.join(self.dir, 'codecased__' + self.input_filename)
        self.ignored_strings = set()
        self.ignored_strings.update(keyword.kwlist)
        self.ignored_strings.update(dir(builtins))
        self.detect_key_strings()

    def detect_key_strings(self):
        with open(self.input_path, "r") as in_file:
            contents = in_file.read()
            for line in contents.splitlines():
                strings = re.split('\W+', line)
                for i, string in enumerate(strings):
                    if string in {'from', 'import', 'class'}:
                        self.ignored_strings.update(strings)

    def process(self, casing_function):
        in_file = open(self.input_path, "r")
        contents = in_file.read()
        in_file.close()

        with open(self.output_path, 'w') as out_file:
            for line in contents.splitlines():
                new_line = str(line)
                for string in re.split('[^.\w+]', line):
                    sdot = string.split('.')
                    if sdot[0] in self.ignored_strings:
                        continue
                    for s in sdot:
                        if s.isupper():
                            continue
                        new_string = casing_function(s)
                        new_line = new_line.replace(s, new_string)
                out_file.write('%s' % new_line + os.linesep)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Change variable casing of your files.")
    parser.add_argument('target_file')
    parser.add_argument('--from_case', default='camel')
    parser.add_argument('--to_case', default='snake')
    parser.add_argument('-i')
    parser.add_argument('--output', default=None)

    args = parser.parse_args()

    codecaser = Codecaser(args.target_file, in_place=args.i, output_filename=args.output)
    codecaser.process(CASING_FUNCTIONS[args.from_case][args.to_case])
