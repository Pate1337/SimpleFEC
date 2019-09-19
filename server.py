import socket
from packet import decode_packet, convert_bytes_to_string, decode_info_packet
from triplepacket import TriplePacket
from xorpacket import XorPacket

class Server(object):
  def __init__(self, host, port):
    self.host = host
    self.port = port
    # Create a UDP socket (SOCK_DGRAM)
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.bind((self.host, self.port))
    self.triplePacket = TriplePacket()
    self.xorPacket = XorPacket()
    self.receivedDataPackets = 0
    self.receivedInfoPackets = 0
    self.packetSize = 104

  def listen(self):
    while True:
      # Receive a message from somewhere
      bytesAddressPair = self.sock.recvfrom(self.packetSize)
      message = bytesAddressPair[0]
      address = bytesAddressPair[1]
      if len(message) == 1:
        # info packet
        self.receive_info_message(message)
        continue
      self.handle_message(message, address)
  
  def receive_info_message(self, message):
    self.receivedInfoPackets += 1
    info_message = convert_bytes_to_string(decode_info_packet(message)[0])
    if info_message == "q":
      self.end_of_file_transmission()
    else:
      self.method = info_message
  
  def end_of_file_transmission(self):
    print()
    print("***************** FINISHED ******************")
    print("Data packets received with triple redundancy:", self.triplePacket.received_packets())
    print("Data packets received with XOR:", self.xorPacket.received_packets())
    print("Total amount of packets received (excluding info packets):", self.receivedDataPackets)
    print("Total amount of info-packets received (1 byte each):", self.receivedInfoPackets)
    print("Total amount of bytes received:", self.amount_of_bytes_received())
    print("*********************************************")
    print()
    self.triplePacket.close()
    self.xorPacket.close()
    self.receivedDataPackets = 0
    self.receivedInfoPackets = 0
    self.triplePacket = TriplePacket()
    self.xorPacket = XorPacket()
  
  def amount_of_bytes_received(self):
    return self.receivedDataPackets * self.packetSize + self.receivedInfoPackets

  def handle_message(self, message, address):
    self.receivedDataPackets += 1
    decoded_data = decode_packet(message)
    if self.method == "t":
      self.triplePacket.receive(message)
    elif self.method == "x":
      self.xorPacket.receive(message)

if __name__ == "__main__":
  port_num = 13445
  host = socket.gethostname()

  Server(host, port_num).listen()