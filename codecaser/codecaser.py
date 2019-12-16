import argparse
import os
import re

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


class Codecaser:

	def __init__(self, target_file, from_case, to_case, ignore_comments=True, in_place=False, destination=None):
		self.from_case = from_case
		self.to_case = to_case
		self.ignore_comments = ignore_comments
		self.in_place = in_place

		in_file = open(target_file, "r")
		self.contents = in_file.read()
		in_file.close()

		self.package_names = set()

		if in_place:
			destination = target_file

		if destination is None:
			self.destination = self.to_case + '__' + target_file.split('/')[-1]
		else:
			self.destination = destination

	def read_packages(self):
		for line in self.contents.splitlines():
			if 'import' in line:
				if 'as' in line:
					package = line.split('as ')[-1].split(' ')[0]
					self.package_names.add(package)
				package = line.split('import ')[-1].split(' ')[0]
				self.package_names.add(package)

	def process(self):
		with open(self.destination, 'w') as out:
			for line in self.contents.splitlines():
				new_line = str(line)
				for string in re.sub("[^a-zA-Z.]+", " ", line).split(' '):
					for substring in string.split('.'):
						if substring in self.package_names:
							continue
						new_line.replace(substring, camel_to_snake(substring))
				out.write('%s' % new_line + os.linesep)


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





