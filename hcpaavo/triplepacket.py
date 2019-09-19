from packet import decode_packet
from filehandling import FileHandling

class TriplePacket(object):
  def __init__(self):
    self.receivedPackets = 0
    self.previouslyReceived = -1
    self.filehandler = FileHandling("data.txt")
  
  def receive(self, packet):
    decoded_data = decode_packet(packet)
    packetNumber = decoded_data[0]
    text = decoded_data[1].decode('utf-8')
    if self.previouslyReceived != packetNumber and self.filehandler.text_matches_file_part((packetNumber - 1) * 100, text):
      self.previouslyReceived = packetNumber
      self.receivedPackets += 1
  
  def received_packets(self):
    return self.receivedPackets
  
  def close(self):
    self.filehandler.close()
    self.receivedPackets = 0
    self.previouslyReceived = -1

