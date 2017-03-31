#!/usr/bin/env python
from sys import argv, stderr
from os import getcwd, path
from subprocess import call

EXPORT_BYTE = 0
EXPORT_STRING = 1

def printUsage():
  print("shellcode_serialise.py [opt] file")
  print("\t-b      as byte array")
  print("\t-s      as string")
  print("\t-v VAR  include variable assignment to VAR")
  print("\t-x      extract .text with objcopy")
  print("\t-h      Print this message")


argc = len(argv)
last = argc - 1
out = ""
var = ""
extract = False


if last == 0:
  printUsage()
  exit()

export = EXPORT_BYTE

for i in  range(0,argc):
  if argv[i] == "-b":
    export = EXPORT_BYTE
  elif argv[i] == "-s":
    export = EXPORT_STRING
  elif argv[i] == "-x":
    extract = True
  elif argv[i] == '-h':
    printUsage()
    exit()
  if i == last: break

  if argv[i] == '-v':
    i = i + 1
    var = argv[i]

fpath = getcwd()+"/"+argv[last]

if not path.isfile(fpath):
  print("Error: file is invalid")
  exit()


if extract:
  fin = fpath
  fpath = fin + ".tmp.bin"
  call(["objcopy", "-O", "binary", "-j", ".text", fin, fpath])

if var:
  out = out + "char " + var +"[] = "

if export == EXPORT_BYTE:
  out = out + "{";
elif export == EXPORT_STRING:
  out = out + "\""

first = True
flen = 0

with open(fpath, "rb") as f:
  while True:
    b = f.read(1)
    if not b: break
    h = ord(b)
    if export == EXPORT_BYTE:
      if flen: out = out +","
      out =  out + "0x{:02x}".format(h)
    elif export == EXPORT_STRING:
      out =  out + "\\x{:02x}".format(h)
    flen = flen + 1

if export == EXPORT_BYTE:
  out = out + "}";
elif export == EXPORT_STRING:
  out = out + "\""

if var:
  out = out + ";"
print(out)


stderr.write("{} bytes\n".format(flen))
