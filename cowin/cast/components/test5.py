import argparse

parser = argparse.ArgumentParser(allow_abbrev=False)
parser.add_argument("-inputpath", help='Please enter input path')
parser.add_argument("-outputpath", help='please enter output Path')
args = parser.parse_args()
print(args)