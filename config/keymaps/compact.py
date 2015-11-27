#!/usr/bin/env python
import sys
import re

TGTWIDTH = 70

try:
    srcname = sys.argv[1]
except IndexError:
    raise Exception('need source filename arg')
dstname = srcname.replace('.xml', '.txt')

src = open(srcname, 'r')
dst = open(dstname, 'w')

for line in src:
    a = re.search('<action id="(.+?)">', line)
    if a:
        action = a.group(1) + ':  '
        bindings = []
    b = re.search(
        '<keyboard-shortcut first-keystroke="(.+?)" '+\
        '(second-keystroke="(.+?)" )?/>', line)
    if b:
        bindings.append(b.group(1))
        if b.group(3):
            bindings[-1] += ', ' + b.group(3)
        bindings[-1] = '({})'.format(bindings[-1])
    if re.search('</action>', line):
        out = action
        for bind in bindings:
            bind += '  '
            if len(out + bind) > TGTWIDTH:
                dst.write(out + '\n')
                out = '    ' + bind
            else:
                out += bind
        dst.write(out + '\n')
            
