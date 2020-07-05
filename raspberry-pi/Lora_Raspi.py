
#this package is in charge of the LoRa communication in none thread way.
#we use the RFM69 package as the LoRa driver.

from RFM69 import Radio, FREQ_915MHZ
import datetime
import time
import comm_manager


node_id = 1 #id in the current network
network_id = 100 #our network id


with Radio(FREQ_915MHZ, node_id, network_id, isHighPower=True, verbose=True) as radio:
    print ("Starting loop...")
    
    rx_counter = 0
    tx_counter = 0  

    while True:
        
        # Every 10 seconds get packets
        if rx_counter > 10:
            rx_counter = 0
            
            # Process packets
            for packet in radio.get_packets():
                comm_manager.analyze_packet(packet)
        # Every 5 seconds send a message
        if tx_counter > 5:
            tx_counter=0

            # Send
            print ("Sending")
            if radio.send(2, "TEST", attempts=3, waitTime=100):
                print ("Acknowledgement received")
            else:
                print ("No Acknowledgement")


        print("Listening...", len(radio.packets), radio.mode_name)
        delay = 0.5
        rx_counter += delay
        tx_counter += delay
        time.sleep(delay)
