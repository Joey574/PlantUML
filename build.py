import os
import re
import argparse

NOTE_BLOCK = re.compile(r"(?ms)^\s*note\b.*?^\s*end\s+note\s*$", re.IGNORECASE)
STRUCT_HEAD = re.compile(r"struct\s+(\w+)\s+{")


def extractStructs(data : str):
    structs = []
    for match in STRUCT_HEAD.finditer(data):
        name = match.group(1)
        bidx = data.find('{', match.start())+1
        idx = bidx
        
        v = 1
        while v != 0:
            if data[idx] == '{':
                v += 1
            elif data[idx] == '}':
                v -= 1
            idx += 1
        
        body = data[bidx:idx-1]
        fbody = [line.strip() for line in body.strip().splitlines() if line.strip()]

        structs.append({"Name": name, "Body": fbody})
        
    return structs

def parseLine(line : str):
    isStatic = False
    isInline = False
    isPublic = False

    parts = line.split()
        
    name = ""
    type = ""
    nextIsType = False

    for token in parts:
        if token == '+':
            isPublic = True
        elif token == '-':
            isPublic = False
        elif token == '{static}':
            isStatic = True
        elif token == '<<inline>>':
            isInline = True
        elif token == ':':
            nextIsType = True
        elif nextIsType:
            type = token
        else:
            name += token + ' '
    
    return {"isPublic": isPublic, "isStatic": isStatic, "isInline": isInline, "Type": type, "Name": name.strip()}

def parseStruct(struct : {str, list[str]}):
    publicProperties = []
    privateProperties = []
    formatted = f'struct {struct["Name"]} ' + '{\n'

    for line in struct["Body"]:
        prop = parseLine(line)
        if prop["isPublic"]:
            publicProperties.append(prop)
        else:
            privateProperties.append(prop)

    publicIdx = 0
    privateIdx = 0

    if len(publicProperties) > 0:
        formatted += "public:\n"
        publicIdx = len(formatted)

    if len(privateProperties) > 0:
        formatted += "private:\n"
        privateIdx = len(formatted)

    formatted += '}\n'

    for p in privateProperties:
        pstr = ""
        if p["isStatic"]:
            pstr += "static "
        if p["isInline"]:
            pstr += "inline "
        
        pstr += (p["Type"] + ' ' + p["Name"] + ';')
        pstr = '\t' + pstr.strip() + '\n'

        formatted = formatted[:privateIdx] + pstr + formatted[privateIdx:]
        privateIdx += len(pstr)
        
    for p in publicProperties:
        pstr = ""
        if p["isStatic"]:
            pstr += "static "
        if p["isInline"]:
            pstr += "inline "
        
        if len(p["Type"]) > 0:
            pstr += p["Type"] + ' ' + p["Name"] + ';'
        else:
            pstr += p["Name"] + ';'

        pstr = '\t' + pstr.strip() + '\n'
            
        formatted = formatted[:publicIdx] + pstr + formatted[publicIdx:]
        publicIdx += len(pstr)

    print(formatted)

parser = argparse.ArgumentParser()
parser.add_argument('main')
args = parser.parse_args()

main = str(args.main)
content = ""

if not os.path.isfile(main):
    exit(1)

with open(main, 'r') as f:
    content = f.read()

    structs = extractStructs(content)
    for s in structs:
        parseStruct(s)


    f.close()
