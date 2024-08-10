import argparse

args = argparse.ArgumentParser(prog="pyls", description="This is a command line program", epilog="This is the complete description")
args.add_argument("-f", "--file", action='store', )

parser = args.parse_args()
print(parser.file)