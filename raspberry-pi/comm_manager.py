
#this packege is for maneging the communication between the server and the raspi

import threading
import queue
import encoder
import requests
import Threading_Lora_Raspi
import aws_connect_and_send

cid = '212' #defualt crane id for testing
srurl = "old server url"  # server url


thread_num = 5

packet_Queue = queue.Queue(1024) #this queue is for incoming messages from the feathers
data_lock =threading.Lock() #lock for synchronine the http messages
status_dict={} #store all the feather's latest messages

#insert feather massage for analyze in the future with the actors
def analyze_packet(packet):
    packet_Queue.put(packet)

#in charge of decode messages from the feather and process them
class Actor_to_server(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    #get message->decode->send to server
    def run(self):
        while True:
            packet = packet_Queue.get()
            packet = encoder.packet_decode(packet)
            data_lock.acquire()
            message_to_server(packet)
            data_lock.release()


#in charge of process messages from the server
class Actor_from_server(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    #TODO: implement get message from server
    def run(self):
        while True:
            if False:
                Threading_Lora_Raspi.message_queue.put("somthing")



#simple processing for tests
def process_packet(threadID,packet):
    print(packet)
    print(threadID)
    status_dict[packet.sender]=packet
    if packet.data==0:
        with open('status.txt', 'w') as f:
            for k, v in status_dict.items():
                 print("id: "+str(k) + " rssi:"+str(v.RSSI)+" data:"+str(v.data)+"\n", file=f)
#list holding all the threads, maybe not necessery
actors =[]


#send message to the old server server using http requests and sending to the new aws using mqtt
def message_to_server(packet):
    print(packet)
    
    msg = {'MessageKind': 'wind', 'WindS': packet.data, 'WindMX': packet.data,
                                'WindMI': packet.data, 'MachineId': cid, 'Index': 2, 'Date': packet.received}
    try:
        #sending http POST to the old server
        r = requests.post(srurl + "/api/SmsR",
                          data=msg)
        aws_connect_and_send.publish(msg)
        print('done!')
        print(r.status_code, r.reason)
        # os.remove(directory + "//" + filename)
    except Exception as e:
        print(e)


#initiate @thread_num actors
for i in range(thread_num):
    actor = Actor_to_server(i)
    actor.start()
    actors.append(actor)
