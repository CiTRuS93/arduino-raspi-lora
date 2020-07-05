
#trasfer two byte into int in 10-base
def packet_decode(packet):
    encoded_num = 0
    for i in range(len(packet.data)):
        encoded_num=encoded_num*100+packet.data[i]
    
    packet.data = encoded_num
    return packet
