#!/usr/bin/env python
import sys

content = ""

for line in sys.stdin:
  content = content + line[:len(line)-1]

if content[0] != '"':
  content = '"' + content

if content[len(content)-1] != '"':
  content = content + '"'

print("$(python -c 'print({})')".format(content))
