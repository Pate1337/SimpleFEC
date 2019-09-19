import socket
from filehandling import FileHandling
from packet import create_packet, create_info_packet, xor
import random

class Client(object):
  def __init__(self, host, port, method, loss):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.serverAddress = (host, port)
    self.method = method
    self.loss = loss
    self.packet_number = 1
  
  def send_file(self):
    # Let's the server know which method is used
    self.acknowledge_server_on_start()
    filehandler = FileHandling("data.txt")
    packetNumber = 0
    text = filehandler.read_bytes(packetNumber * 100)
    while text:
      # Now there is data to be sent, next we need to modify it into a packet
      if self.method == "triple":
        self.handle_triple_packet(text)
      elif self.method == "xor":
        self.handle_xor_packet(text)
      packetNumber += 1
      text = filehandler.read_bytes(packetNumber * 100)
    print()
    print("Original data packets sent:", packetNumber)
    if self.method == "triple":
      print("Total amount of packets sent:", (self.packet_number - 1) * 3)
    elif self.method == "xor":
      print("Total amount of packets sent:", self.packet_number - 1)
    print()
    self.acknowledge_server_on_end()
    self.sock.close()
    filehandler.close()
  
  def handle_triple_packet(self, text):
    # Create 3 packets and send all of them
    for i in range(3):
      data = create_packet(self.packet_number, text)
      self.send_packet(data, self.loss)
    self.packet_number += 1
  
  def handle_xor_packet(self, text):
    if self.packet_number % 3 == 1:
      # packetA
      data = create_packet(self.packet_number, text)
      self.packetA_text = text
    elif self.packet_number % 3 == 2:
      # packetB
      data = create_packet(self.packet_number, text)
      self.packetB_text = text

    self.send_packet(data, self.loss)
    self.packet_number += 1

    if self.packet_number % 3 == 0:
      # packetA and packetB has been sent, need to create packetC and send it
      packetC = xor(self.packetA_text, self.packetB_text)
      data = create_packet(self.packet_number, packetC)
      self.send_packet(data, self.loss)
      self.packet_number += 1

  
  def send_packet(self, data, loss):
    if not self.packet_lost(loss):
      self.sock.sendto(data, self.serverAddress)
  
  def packet_lost(self, loss):
    random_number = random.randint(1,100)
    if random_number > loss:
      return False
    return True
  
  def acknowledge_server_on_start(self):
    m = "x"
    if self.method == "triple":
      m = "t"
    packet = create_info_packet(m)
    self.sock.sendto(packet, self.serverAddress)
  
  def acknowledge_server_on_end(self):
    packet = create_info_packet("q")
    self.sock.sendto(packet, self.serverAddress)


def ask_method():
  method = ""
  while True:
    method = input("Choose a variant of FEC:\n(1) Triple redundancy\n(2) XOR\n")
    if method == "1":
      method = "triple"
      return method
    elif method == "2":
      method = "xor"
      return method

def ask_loss_rate():
  loss = 0
  while True:
    user_input = input("\nGive the package loss rate (0 - 100)\n")
    try:
      loss = int(user_input)
      if loss >= 0 and loss <= 100:
        return loss
      else: raise ValueError
    except ValueError:
      print("Must be a number between 0 and 100!")

if __name__ == "__main__":
  method = ask_method()
  loss = ask_loss_rate()

  host = socket.gethostname()
  port = 13445
  Client(host, port, method, loss).send_file()