from packet import decode_packet, xor, convert_bytes_to_string
from filehandling import FileHandling
import math

class XorPacket(object):
  def __init__(self):
    self.receivedPackets = 0
    self.filehandler = FileHandling("data.txt")
    self.previouslyReceivedA = (-1, "none")
    self.previouslyReceivedB = (-1, "none")
  
  def receive(self, packet):
    decoded_data = decode_packet(packet)
    packetNumber = decoded_data[0]
    text = convert_bytes_to_string(decoded_data[1])
    if packetNumber % 3 == 1:
      # packetA
      self.previouslyReceivedA = decoded_data
      if self.received_package_is_legit(packetNumber, text):
        self.receivedPackets += 1
    elif packetNumber % 3 == 2:
      # packetB
      self.previouslyReceivedB = decoded_data
      if self.received_package_is_legit(packetNumber, text):
        self.receivedPackets += 1
    else:
      # packetC
      if self.previouslyReceivedA[0] + 2 == packetNumber and self.previouslyReceivedB[0] + 1 != packetNumber:
        # We can get packetB with A and C
        packetB = xor(convert_bytes_to_string(self.previouslyReceivedA[1]), text)
        if self.received_package_is_legit(packetNumber - 1, packetB):
          self.receivedPackets += 1
      elif self.previouslyReceivedB[0] + 1 == packetNumber and self.previouslyReceivedA[0] + 2 != packetNumber:
        # We can get packetA with B and C
        packetA = xor(convert_bytes_to_string(self.previouslyReceivedB[1]), text)
        if self.received_package_is_legit(packetNumber - 2, packetA):
          self.receivedPackets += 1
  
  def received_package_is_legit(self, packetNumber, text):
    amount_of_c_packets = math.floor(packetNumber / 3)
    return self.filehandler.text_matches_file_part((packetNumber - amount_of_c_packets - 1) * 100, text)
  
  def received_packets(self):
    return self.receivedPackets
  
  def close(self):
    self.filehandler.close()
    self.receivedPackets = 0
    self.previouslyReceivedA = (-1, "none")
    self.previouslyReceivedB = (-1, "none")