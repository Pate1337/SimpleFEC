import struct

def create_packet(number, content):
  values = (number, content.encode())
  packer = struct.Struct('I 100s')
  packed_data = packer.pack(*values)

  #print(packed_data)
  return packed_data

def decode_packet(bytes):
  unpacker = struct.Struct('I 100s')
  unpacked_data = unpacker.unpack(bytes)
  # returns a tuple (Integer, bytes)
  return unpacked_data

def convert_bytes_to_string(bytes):
  return bytes.decode('utf-8')

def convert_string_to_binary(text):
  binary = "".join(f"{ord(i):08b}" for i in text)
  return binary

def create_info_packet(method):
  # triple = t and xor = x
  packer = struct.Struct('1s')
  packed_data = packer.pack(method.encode())
  return packed_data

def decode_info_packet(bytes):
  unpacker = struct.Struct('1s')
  unpacked_data = unpacker.unpack(bytes)
  return unpacked_data

def xor(packetA, packetB):
  #print(packetA)
  #print(packetB)
  #print(packetA)
  #print(packetB)
  #b1 = bytearray(packetA, "utf-8")
  #print(b1)
  #b2 = bytearray(packetB, "utf-8")
  #print(b2)
  #b = bytearray(len(b1))
  #for i in range(len(b1)):
  #  b[i] = b1[i] ^ b2[i]
  #print(b)
  #b3 = bytearray(2)
  #b3[0] = 140
  #print(b3)
  #decode_bytes(b1)
  #decode_bytes(b2)
  #decode_bytes(b3)

  xor_bytes = sxor(packetA, packetB)
  #print(len(xor_bytes))
  #print("xor_bytes: ", xor_bytes)
  #packetA_content_in_bytes = decode_packet(packetA)[1]
  #packetB_content_in_bytes = decode_packet(packetB)[1]
  #print("packetA content in bytes: ", packetA_content_in_bytes)
  #print("packetB content in bytes: ", packetB_content_in_bytes)
  #xor_bytes = byte_xor(packetA_content_in_bytes, packetB_content_in_bytes)
  #print("xor_bytes: ", xor_bytes)
  #print("50 in bytes: ", bytes([50]))
  #xor_bytes = bytes([packetA_content_in_bytes[0] ^ packetB_content_in_bytes[0]])
  #for i in range (1, len(packetA_content_in_bytes)):
  #  print("packetA: ", bytes([packetA_content_in_bytes[i]]))
  #  print("packetB: ", bytes([packetB_content_in_bytes[i]]))
  #  print("xor: ", bytes([packetA_content_in_bytes[i] ^ packetB_content_in_bytes[i]]))
  #  xor_bytes += bytes([packetA_content_in_bytes[i] ^ packetB_content_in_bytes[i]])
  #print("whole xor: ", xor_bytes.decode('utf-8'))
  return xor_bytes

def decode_bytes(bytes):
  print(bytes.decode('utf-8'))

def byte_xor(ba1, ba2):
  return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def sxor(s1,s2):    
  return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

# 00101100 ^ 10010011 = 10111111