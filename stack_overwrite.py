#!/usr/bin/env python
import argparse


parser = argparse.ArgumentParser(description='Generate data to overflow a stack and, optionally, write 8-bit hexidecimal bytes at particular offset')

parser.add_argument('size', metavar='SIZE', type=int,
                    help='The size to overwrite')

parser.add_argument('sequence', metavar='SEQ', nargs='?', default='',
                    help='The hexidecimal byte sequence to place at offset SIZE')

parser.add_argument('-op', '--output-python', dest='output', default='python', action="store_const", const='python',
                    help='Specify output format as expandable python (default)')

parser.add_argument('-os', '--output-cstr', dest='output', action="store_const", const='cstr',
                    help='Specify output as an expanded C style string')

parser.add_argument('-ob', '--output-cbyte', dest='output', action="store_const", const='cbyte' ,
                    help='Specify output as an expanded C style byte array')

parser.add_argument('-j', '--junk', dest='junk', action="store", default="00",
                    help='Set the hexadecimal junk value')

parser.add_argument('-v', '--var', dest='var', action="store", default="",
                    help='Assign output to a variable')


args = parser.parse_args()




def to_bytes(bstr):
  out = []
  step = 2
  inc = 2

  for i in range( 0, len(bstr), step ):
    out.append( int( bstr[i:i+inc], 16 ) )

  return list( reversed(out) )

str_out = ""
junk_int = int(args.junk, 16)
seq_bytes = to_bytes(args.sequence)


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
