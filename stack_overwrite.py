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


def output_python(size, junk, seq_bytes):
  seq_str =  '+"{}"'.format("".join(map(lambda b: "\\x{:02x}".format( b ),  seq_bytes ))) if args.sequence else ""
  return '"\\x{}"*{}'.format(junk,  size) + seq_str

def output_cstr(size, junk, seq_bytes):
  return '"{}"'.format( "".join( [ "\\x{:02x}".format( junk ) ] * size + map(lambda b: "\\x{:02x}".format( b ),  seq_bytes ) ) )

def output_cbyte(size, junk, seq_bytes):
  return '{{{}}}'.format( ",".join( [ "0x{:02x}".format( junk ) ] * size + map(lambda b: "0x{:02x}".format( b ),  seq_bytes ) ) )


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


parser.add_argument('-op', '--output-python', dest='output', default=output_python, action="store_const", const=output_python,
                    help='Specify output format as expandable python (default)')

parser.add_argument('-os', '--output-cstr', dest='output', action="store_const", const=output_cstr,
                    help='Specify output as an expanded C style string')

parser.add_argument('-ob', '--output-cbyte', dest='output', action="store_const", const=output_cbyte ,
                    help='Specify output as an expanded C style byte array')



parser.add_argument('-j', '--junk', dest='junk', action="store", default="00",
                    help='Set the hexadecimal junk value (default 00)')


parser.add_argument('-v', '--var', dest='var', action="store", default="",
                    help='Assign output to a variable')


args = parser.parse_args()





str_out = args.output(args.size, int(args.junk, 16), args.conv(args.sequence, args.keep) )

if args.var:
  str_out = "{}={}".format(args.var, str_out)

print(str_out)
