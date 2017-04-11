#!/usr/bin/env python
import sys


def generatePattern(size):
  pattern = []

  lower = 0x61
  upper = 0x41
  numeric = 0x30
  phase = 0

  for i in range(0,size):
    if phase == 0:
      pattern.append(upper)
      phase = 1
    elif phase == 1:
      pattern.append(lower)
      phase = 2
    elif phase == 2:
      pattern.append(numeric)
      phase = 0

    numeric = numeric + 1 if numeric < 0x39 else 0x30
    if numeric == 0x30:
      lower = lower + 1  if lower < 0x7E else 0x61
      if lower == 0x61:
        upper = upper + 1  if upper < 0x61 else 0x41

  return pattern

def stringBytesToIntArray(bstr, little = False):
  interim  = []
  a = []
  for i in range(0, len(bstr), 2):
    interim.append( "".join(bstr[i:i+2]) )

  interim = interim if little == False else list(reversed(interim))

  for i in range(0, len(interim)):
    a.append( int(interim[i], 16) )

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
  print("\tgenerate   Generate a pattern of given size")
  print("\tfind       Find offset of sequence in pattern")
  print("\nopts:")
  print("\t-s, --size BYTES    Generate pattern to size BYTES")
  print("\t-p, --pattern PAT   sequence PAT to find in pattern")
  print("\t-l, --little        little-endian sequence pattern")
  print("\t-h, --help          Print this message")
    

size = 0
pattern = ""
little = False

argc = len(sys.argv)
last = argc-1

if last == 0:
  printUsage()
  exit(1)

cmd = sys.argv[1]

if cmd == "-h" or cmd == "--help":
  printUsage()
  exit(0)

if cmd != "generate" and cmd != "find":
  print("Error: unrecognised command " + cmd)
  printUsage()
  exit(1)

for i in range(2, argc):
  arg = sys.argv[i]
  if arg == '-l' or arg == "--little":
    little = True

  if i == last: break

  if arg == "-s" or arg == "--size":
    i = i + 1;
    size = int(sys.argv[i])
  elif arg == "-p" or arg == "--pattern":
    i = i + 1;
    pattern = sys.argv[i]
  elif arg == "-h" or arg == "--help":
    printUsage()
    exit(0)
    


if cmd == "generate":
  print("".join(chr(x) for x in generatePattern(size)))
elif cmd == "find":

  b = findSequence(pattern, generatePattern(size), little) 
  if b > -1:
    print("Byte offset: {}".format(b))
  else:
    print("Sequence not found")
  
