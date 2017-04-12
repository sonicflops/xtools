#!/usr/bin/env python
import argparse

def hex_to_bytes(bstr, keep_endian):
  out = []
  step = 2
  inc = 2

  for i in range( 0, len(bstr), step ):
    out.append( int( bstr[i:i+inc], 16 ) )

  return list( reversed(out) ) if not keep_endian else list(out)


  
def ascii_to_bytes(bstr, keep_endian):
  out = []
  step = 2
  inc = 2

  out = map( lambda b: ord(b),  bstr)

  return list( reversed(out) ) if not keep_endian else list(out)


parser = argparse.ArgumentParser(description='Generate data to overflow a stack and, optionally, write the bytes at particular offset. The byte sequence will be rearrange into little endian unless told otherwise')

parser.add_argument('size', metavar='SIZE', type=int,
                    help='The size to overwrite')

parser.add_argument('sequence', metavar='SEQ', nargs='?', default='',
                    help='The byte sequence to place at offset SIZE')

parser.add_argument('-k', '--keep', dest='keep', action="store_true", default=False,
                    help='Keep the endian of the byte sequence')

parser.add_argument('-ix', '--input-hex', dest='conv', action="store_const", const=hex_to_bytes, default=hex_to_bytes,
                    help='The byte sequence is a hexadecimal string (default)')

parser.add_argument('-ia', '--input-ascii', dest='conv', action="store_const", const=ascii_to_bytes,
                    help='The byte sequence is an ASCII string')


parser.add_argument('-op', '--output-python', dest='output', default='python', action="store_const", const='python',
                    help='Specify output format as expandable python (default)')

parser.add_argument('-os', '--output-cstr', dest='output', action="store_const", const='cstr',
                    help='Specify output as an expanded C style string')

parser.add_argument('-ob', '--output-cbyte', dest='output', action="store_const", const='cbyte' ,
                    help='Specify output as an expanded C style byte array')



parser.add_argument('-j', '--junk', dest='junk', action="store", default="00",
                    help='Set the hexadecimal junk value (default 00)')


parser.add_argument('-v', '--var', dest='var', action="store", default="",
                    help='Assign output to a variable')


args = parser.parse_args()




str_out = ""
junk_int = int(args.junk, 16)
seq_bytes =args.conv(args.sequence, args.keep)


if args.output == 'python':
  seq_str =  '+"{}"'.format("".join(map(lambda b: "\\x{:02x}".format( b ),  seq_bytes ))) if args.sequence else ""
  str_out = '"\\x{}"*{}'.format(args.junk,  args.size) + seq_str
elif args.output == 'cstr':
  str_out = '"{}"'.format( "".join( [ "\\x{:02x}".format( junk_int ) ] * args.size + map(lambda b: "\\x{:02x}".format( b ),  seq_bytes ) ) )
elif args.output == 'cbyte':
  str_out = '{{{}}}'.format( ",".join( [ "0x{:02x}".format( junk_int ) ] * args.size + map(lambda b: "0x{:02x}".format( b ),  seq_bytes ) ) )

if args.var:
  str_out = "{}={};".format(args.var, str_out)

print(str_out)
