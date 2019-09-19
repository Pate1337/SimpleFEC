import struct

def create_packet(number, content):
  values = (number, content.encode())
  packer = struct.Struct('I 100s')
  packed_data = packer.pack(*values)

  return packed_data

def decode_packet(bytes):
  unpacker = struct.Struct('I 100s')
  unpacked_data = unpacker.unpack(bytes)
  # returns a tuple (Integer, bytes)
  return unpacked_data

def convert_bytes_to_string(bytes):
  return bytes.decode('utf-8')

def create_info_packet(method):
  # triple = t and xor = x
  packer = struct.Struct('1s')
  packed_data = packer.pack(method.encode())
  return packed_data

def decode_info_packet(bytes):
  unpacker = struct.Struct('1s')
  unpacked_data = unpacker.unpack(bytes)
  return unpacked_data

def sxor(s1,s2):    
  return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))
