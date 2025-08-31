import os
import argparse


def cleanFile(data : str):
    data = data[data.find('\n'):data.rfind('@')]
    return data


parser = argparse.ArgumentParser()
parser.add_argument('main')
args = parser.parse_args()

main = str(args.main)
dir = main[:main.rfind('/')]
content = ""

if not os.path.isfile(main):
    exit(1)

with open(main, 'r') as f:
    content = f.read()
    f.close()

while content.find("!include") != -1:
    idx = content.find("!include") + len("!include") + 1
    filename = content[idx:content.find('\n', idx)]

    path = dir+'/'+filename

    with open(path, 'r') as f:
        content = content.replace('!include ' + filename, cleanFile(f.read()))
        f.close()

print(content)
