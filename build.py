import os
import argparse

def parseStruct(struct : str):
    name = struct[struct.find(' '):struct.find('{')]

parser = argparse.ArgumentParser()
parser.add_argument('main')
args = parser.parse_args()

main = str(args.main)
content = ""

if not os.path.isfile(main):
    exit(1)

with open(main, 'r') as f:
    content = f.read()
    f.close()


print(content)
