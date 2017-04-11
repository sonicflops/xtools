#!/usr/bin/env python
import sys, base64, fileinput

def stringBytesToIntArray(bstr):
  interim  = []
  a = []
  for i in range(0, len(bstr), 2):
    interim.append( "".join(bstr[i:i+2]) )

  interim = list(reversed(interim))

  for i in range(0, len(interim)):
    a.append( int(interim[i], 16) )

  return a

def generateBytes(pattern):
  return  stringBytesToIntArray(pattern)
  
def printUsage():
  print("usage: stack_levalue.py PATTERN [opts]")
  print("\t-b64, --base64   Convert output to base64")
  print("\t-s, --string     Output as a string array")
  print("\t-b, --byte       Output as a string array")
  print("\t-h, --help       Print this message")
pattern = ""
output = 'string'

argc = len(sys.argv)
last = argc-1


if argc < 2:
  printUsage()
  exit(1)

if argc == 2 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
  printUsage();
  exit(0)


pattern = sys.argv[1]

argi = 0

for i in range(2,argc):
  arg = sys.argv[i]
  if arg == "-s" or arg == "--string":
    output = "string"
  elif arg == "-b" or arg == "--byte":
    output = "byte"
  elif arg == "-h" or arg == "--help":
    printUsage()
    exit(0)

binVals = generateBytes(pattern)
out = ""
if output == "string":
  out = "\""
  for b in binVals:
    out = out + "\\x{:02x}".format(b)
  out = out + "\""
else:
  out = "["
  for b in binVal:
    out = out + "0x{:02x},".format(b)
  out = out + "]"
  
print(out)
