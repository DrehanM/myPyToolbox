import argparse
import re

PATTERNS = {
	'camel': r'(([a-z]+)([A-Z][A-Za-z]*))',
	'snake': r'(([a-z]+)_([a-z]+))',
}


def process(args):
	if args.i:
		output_file = args.target_file
	else:
		output_file = args.to_case + '__' + args.target_file

	in_file = open(args.target_file, "r")
	contents = in_file.read()

	in_file.close()

	with open(output_file, 'w') as out:
		for line in contents.splitlines():
			new_line = []
			for string in line.split(' '):
				new_string = change_casing(string, args)
				new_line.append(new_string)
			out.write('%s/n' % ' '.join(new_line))

# Need to account for quotations, punctuation, etc.
def change_casing(string, args):
	pattern = PATTERNS[args.from_case]
	matches = re.match(pattern, string).groups()

	if len(matches) == 0:
		return string

	#if args.to_case == 'snake':
	cased_string = re.sub(pattern, '_'.join(matches[1:], string))

	return cased_string


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Change variable casing of your files.")
	parser.add_argument('target_file')
	parser.add_argument('--from_case', default='camel')
	parser.add_argument('--to_case', default='snake')
	parser.add_argument('-i')

	args = parser.parse_args()

	process(args)





