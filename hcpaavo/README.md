# Forward Error Correction

This project demonstrates sending a file from sender (client) to receiver (server) using UDP. User can choose between two variants of forward error correction (FEC):
1. Triple redundancy, where each packet is sent 3 times.
2. XOR, which calculates the exlusive OR of packets A and B, and names this packet C. The packets are sent in order A, B and C.

User can also choose to inject packet loss, between 0 and 100 percents.

## How to run the program?

Unzip the file "hcpaavo_NSS19_EX.zip".
Go to the unzipped folder, and navigate to subdirectory /hcpaavo.
To start the server, run the command 
```
python3 server.py
```
The server is now running. Open a new terminal window, and navigate to locaction /hcpaavo.
To start the client, run the command
```
python3 client.py
```

client.py contains the ui for the program.

After sending the file from client, you can view the received data from the terminal window, where the server is running.


## How is the packet loss implemented?

Packet loss is implemented simply by not sending the individual packet, if a randomly generated number between 1 and 100 is equal or smaller than the given loss rate. Packet loss is therefore injected in the client.py-file.

## How to know which packets are received succesfully?

The program simply checks the data of the packets received, and compares it to the corresponding text of the file. The file is read in both client and server.

## What is the overhead caused by both FEC variants?

For every packet, containing 100 bytes of the original data (from file), there are 4 additional bytes added to indicate the packet number. Every packet sent from the client is therefore 104 bytes in total so the total rate of code is 100/104 = 25/26, which is about 0,96.

Before sending the file, the server is informed of the selected FEC with an info packet, which has a size of 1 byte. Also after the file is sent, the server is again informed with another info packet of 1 byte. So a total of 2 bytes is added to total overhead.

Let's assume the number of original data packets to be sent is k. The overhead caused by packet numbers and info packets is therefore:
```
overhead = 4 * k + 2
```
bytes.

### Triple redundancy

Triple redundancy simply sends every packet 3 times. So the total overhead for sending a file is:
```
overhead = 4 * k * 3 + 2 * k * n + 2, where n is the size of the packet in bytes
```
bytes.

### XOR

XOR creates a redundant packet C, which is the result of exclusive OR of packets A and B. Packet C has the same size as packets A and B, so the total overhead for XOR is:
```
overhead = 4 * (k + floor(k / 2)) + floor(k / 2) * n + 2, where floor(k / 2) is the number of redundant C packets and n is the size of the packet in bytes
```
bytes.

## How does	increasing loss rate affect the	success	rate of	decoding?

The graph below shows the success rate as a function of the loss rate for both FECs.
<img src="https://raw.githubusercontent.com/Pate1337/SimpleFEC/master/successrates.png" width="750">

The graph is located in /hcpaavo/successrates.png.

