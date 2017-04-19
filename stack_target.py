#!/usr/bin/env python

import argparse

def generate_pattern(size):
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

def hex_to_bytes(bstr, keep_endian):
  out = []
  step = 2
  inc = 2

  for i in range( 0, len(bstr), step ):
    out.append( int( bstr[i:i+inc], 16 ) )

  return list( reversed(out) ) if not keep_endian else list(out)

def ascii_to_bytes(bstr, keep_endian):
  out = map( lambda b: ord(b),  bstr)

  return list( reversed(out) ) if not keep_endian else list(out)

  
def locate_sequence(size, sequence):
  pattern = generate_pattern(size)
  last_seq = len(sequence) - 1
  last_pat = len(pattern) - 1

  for i in range(0, len(pattern)):
    start_byte = i
    for j in range(0, len(sequence)):
      if pattern[i] == sequence[j]:
        if j == last_seq:
          return start_byte

        if i == last_pat: return -1
        i = i + 1
      else: break

  return -1
  

parser = argparse.ArgumentParser(description='Generate data pattern to overflow stack or find offset of a point in that pattern')

parser.add_argument('size', metavar='SIZE', type=int,
                    help='The number of bytes to generate in pattern')

parser.add_argument('-f', '--find', dest='sequence', metavar="SEQ", default='', action="store",
                    help='The byte sequence to find')

parser.add_argument('-k', '--keep', dest='keep_endian', default=False, action="store_true",
                    help='Keep the endian of the byte sequence')

parser.add_argument('-ix', '--input-hex', dest='conv', default=hex_to_bytes, action="store_const", const=hex_to_bytes,
                    help='The input sequence is a hexadecimal string (default)')

parser.add_argument('-ia', '--input-ascii', dest='conv', const=ascii_to_bytes, action="store_const",
                    help='The input sequence is an ASCII string')

args = parser.parse_args()



if args.sequence:
  bytes = args.conv(args.sequence, args.keep_endian)
  bytes_str = " ".join(map(lambda b: chr(b),  bytes))
  offset = locate_sequence( args.size, args.conv(args.sequence, args.keep_endian) )
  if offset >= 0:
    print( "Sequence {}\noffset: {} bytes".format(bytes_str, offset) )
  else:
    print( "Sequence {}\nNot found".format( bytes_str ) )
else:
  print( "{}".format( "".join( map(lambda b: chr(b),  generate_pattern(args.size)) ) ) )

