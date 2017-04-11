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

def generateOverflowSeq(offset, pattern, little = False, junk = "0"):
  hexPattern = map( lambda p: stringBytesToIntArray(p, little),  pattern )
  output = []
  for _ in range(0, offset):
    output.append(int(junk,16))
  output = output + reduce( lambda p1,p2: p1 + p2, hexPattern ) 

  return output
  
def printUsage():
  print("usage: stack_overwrite.py OFFSET PATTERN [PATTERN ...] [opts]")
  print("\t-l, --little     Reformat PATTERN into little endian")
  print("\t-b64, --base64   Convert output to base64")
  print("\t-j, --junk       Junk byte to use for padding")
  print("\t-h, --help       Print this message")
  print("\t-s, --string     Print as string")
size = 0
pattern = []
little = False
b64 = False
out = "bin"
junk = "0"

argc = len(sys.argv)
last = argc-1

if argc == 2 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
  printUsage();
  exit(0)

if argc < 3:
  printUsage()
  exit(1)

offset = int(sys.argv[1])
pattern.append(sys.argv[2])

argi = 0

for argi in range(3,argc):
  arg = sys.argv[argi]
  if arg[0] == '-':
    break
  
  if arg[0] == "\\":
    arg = arg[1:]

  pattern.append(arg)

for i in range(argi,argc):
  arg = sys.argv[i]
  if arg == "-l" or arg == "--little":
    little = True
  elif arg == "-b64" or arg == "--base64":
    b64 = True
  elif arg == "-s" or arg == "--string":
    out = "string"
  elif arg == "-h" or arg == "--help":
    printUsage()
    exit(0)

  if i == last:
    break
  
  if arg == "-j" or arg == "--junk":
    i = i + 1
    if sys.argv[i] == "":
      continue

    junk = sys.argv[i]
    

binVals = generateOverflowSeq(offset,pattern,little, junk)
strVals = "".join( chr(x) for x in binVals )

if b64 == True:
  print( base64.b64encode(strVals) )
else:
  if out == "bin":
    print( strVals  )
  elif out == "string":
    print( "\"" + "".join( "\\x{:02x}".format(x) for x in binVals ) + "\"")
