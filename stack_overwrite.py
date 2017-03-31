#!/usr/bin/env python
import sys, base64, fileinput

def stringBytesToIntArray(bstr, little = False):
  interim  = []
  a = []
  for i in range(0, len(bstr), 2):
    interim.append( "".join(bstr[i:i+2]) )

  interim = interim if little == False else list(reversed(interim))

  for i in range(0, len(interim)):
    a.append( int(interim[i], 16) )

  return a

def generateOverflowSeq(offset, pattern, little = False):
  hexPattern = stringBytesToIntArray(pattern, little)
  output = []
  for _ in range(0, offset):
    output.append(0x30)

  output = output + hexPattern

  return output
  
def printUsage():
  print("usage: stack_overwrite.py OFFSET PATTERN [opts]")
  print("\t-l, --little     Reformat PATTERN into little endian")
  print("\t-b64, --base64   Convert output to base64")
  print("\t-h, --help       Print this message")
size = 0
pattern = ""
little = False
b64 = False

argc = len(sys.argv)
last = argc-1

if argc == 2 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
  printUsage();
  exit(0)

if argc < 3:
  printUsage()
  exit(1)

offset = int(sys.argv[1])
pattern = sys.argv[2]

for i in range(3,argc):
  arg = sys.argv[i]
  if arg == "-l" or arg == "--little":
    little = True
  elif arg == "-b64" or arg == "--base64":
    b64 = True
  elif arg == "-h" or arg == "--help":
    printUsage()
    exit(0)

binVals = generateOverflowSeq(offset,pattern,little)
strVals = "".join( chr(x) for x in binVals )

if b64 == True:
  print( base64.b64encode(strVals) )
else:
  print( strVals  )
