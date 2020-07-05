
#this package is in charge of the LoRa communication in threads way.
#we use the RFM69 package as the LoRa driver.


from RFM69 import Radio, FREQ_915MHZ
import datetime
import time
import comm_manager
import threading
import queue

node_id = 1 #id in the current network
network_id = 100 #our network id
message_queue = queue.Queue(1024) #queue for incoming messages from the server

#this thread is incharge of the incoming transmit from the feathers.
#and transfer the messages to the comm manager for process
class Reciever(threading.Thread):
    def __init__(self, radio):
        threading.Thread.__init__(self)
        self.radio = radio
    def run(self):
        while True:
            if  self.radio.has_received_packet():
                for packet in self.radio.get_packets():
                    print(packet)
                    comm_manager.analyze_packet(packet)



#this thread is incharge of sending messages to the feathers.
class Transmitter(threading.Thread):
    def __init__(self, radio):
        threading.Thread.__init__(self)
        self.radio = radio
    def run(self):
        while True:
            message = message_queue.get()
            if self.radio.send(2, "TEST", attempts=3, waitTime=100):
                print ("Acknowledgement received")
            else:
                print ("No Acknowledgement")
                



with Radio(FREQ_915MHZ, node_id, network_id, isHighPower=True, verbose=True) as radio:
    print ("Starting loop...")
    #initiating the threads
    reciever = Reciever(radio)
    transmitter = Transmitter(radio)
    reciever.start()
    reciever.join()
