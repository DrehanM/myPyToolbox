import argparse
import re


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Change variable casing of your files.")
	parser.add_argument('target')
	parser.add_argument('from_case')
	parser.add_argument('to_case')

	target, from_case, to_case = parser.parse_args()



