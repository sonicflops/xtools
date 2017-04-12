#!/usr/bin/env python
import sys


def generatePattern(size):
  pattern = []

  lower = 0x61
  upper = 0x41
  numeric = 0x30
  phase = 0
  diff = size % 3
  rounded = size + (3-diff)
  for i in range(0, rounded):
    pattern.append(upper)
    pattern.append(lower)
    pattern.append(numeric)

    numeric = numeric + 1 if numeric < 0x39 else 0x30
    if numeric == 0x30:
      lower = lower + 1  if lower < 0x7E else 0x61
      if lower == 0x61:
        upper = upper + 1  if upper < 0x61 else 0x41

  return pattern[:size]

def stringBytesToIntArray(bstr, ptype):

  interim  = []
  a = []
  if ptype == 'memory':
    for i in range(0, len(bstr), 2):
      interim.append( "".join(bstr[i:i+2]) )
    interim = list(reversed(interim))
    for i in range(0, len(interim)):
      a.append( int(interim[i], 16) )
  else:
    for c in bstr:
      a.append(ord(c))

  return a


def findSequence(needle, haystack, little = False):
  needleInt = stringBytesToIntArray(needle, little)
  last = len(needleInt) - 1
  lastHay = len(haystack) - 1
  for i in range(0, len(haystack)):
    startByte = i

    for j in range(0, len(needleInt)):
      if haystack[i] == needleInt[j]:
        if j == last:
          return startByte

        if i == lastHay: return -1
        i = i + 1
      else: break

  return -1
      
def printUsage():
  print("usage: stack_overflow_target.py command [-opts]")
  print("command:")
  print("\tgenerate SIZE       Generate a pattern of given size")
  print("\tfind SIZE PATTERN   Find offset of pattern")
  print("\nopts:")
  print("\t-m, --memory        Convert pattern from memory dump")
  print("\t-s, --string        Convert pattern to string")
  print("\t-h, --help          Print this message")
    

size = 0
pattern = ""
ptype = 'memory'

argc = len(sys.argv)
last = argc-2

if last == 0:
  printUsage()
  exit(1)

cmd = sys.argv[1]
size = int(sys.argv[2])


if cmd == "-h" or cmd == "--help":
  printUsage()
  exit(0)


if cmd != "generate" and cmd != "find":
  print("Error: unrecognised command " + cmd)
  printUsage()
  exit(1)

if cmd == "find":
  pattern = sys.argv[3]


for i in range(4, argc):
  arg = sys.argv[i]
  if arg == '-m' or arg == "--memory":
    ptype = 'memory'
  elif arg == '-s' or arg == '--string':
    ptype = 'string'

  if i == last: break

  if arg == "-h" or arg == "--help":
    printUsage()
    exit(0)
    

if cmd == "generate":
  print("".join(chr(x) for x in generatePattern(size)))
elif cmd == "find":

  b = findSequence(pattern, generatePattern(size), ptype) 
  if b > -1:
    print("[{}] Byte offset: {}".format(ptype,b))
  else:
    print("[{}] Sequence `{}` not found".format(ptype,pattern))
  
