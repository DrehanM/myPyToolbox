import argparse
import os
import re

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

def camel_to_snake(string):
	s1 = first_cap_re.sub(r'\1_\2', string)
	return all_cap_re.sub(r'\1_\2', s1).lower()


def snake_to_camel(string):
	pass


def process(args):
	if args.i:
		output_file = args.target_file
	else:
		output_file = args.to_case + '__' + args.target_file.split('/')[-1]

	in_file = open(args.target_file, "r")
	contents = in_file.read()

	in_file.close()

	with open(output_file, 'w') as out:
		for line in contents.splitlines():
			new_line = str(line)
			for string in re.split('\W+', line):
				new_string = change_casing(string, args)
				new_line = new_line.replace(string, new_string)
			out.write('%s' % new_line + os.linesep)


'''def process_line(line):
	new_line = str(line)
	split_line = re.split(re.sub("[^a-zA-Z.]+", " ", line), ' ')
	for string in split_line:'''


# Need to account for quotations, punctuation, etc.
def change_casing(string, args):
	if args.to_case == 'snake':
		return camel_to_snake(string)
	elif args.to_case == 'camel':
		return snake_to_camel(string)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Change variable casing of your files.")
	parser.add_argument('target_file')
	parser.add_argument('--from_case', default='camel')
	parser.add_argument('--to_case', default='snake')
	parser.add_argument('-i')

	args = parser.parse_args()

	process(args)





