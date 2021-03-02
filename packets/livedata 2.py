import socket
import struct

from f1_2020_telemetry.packets import unpack_udp_packet

udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_socket.bind(("", 20777))

_noupdate = None
_weather = 10
while True:
    udp_packet = udp_socket.recv(2048)
    packet = unpack_udp_packet(udp_packet)
    if packet.header.packetId == 1: #session packet
        if _weather != _noupdate:
            track = packet.trackId
            _weather = packet.weather
            _noupdate = _weather

            if _weather == 5:
                print("its Wet, storm")

            print("weather: ", _weather, " track: ",  track) #-1 for unknown, 0-21 for tracks
    
    
    #if packet.header.packetId == 2: #Lap Data packet
    #if packet.header.packetId == 3: #Event  packet 
     #   print(packet)
    #if packet.header.packetId == 4: #Participants  packet
    
    #if packet.header.packetId == 5: #carsetup packet -useless
    #if packet.header.packetId == 6: #Car Telemetry packet
    #if packet.header.packetId == 7: #Car Status packet
    if packet.header.packetId == 8: #Final Classification  packet
        print(packet)
    #if packet.header.packetId == 9: #lobby packet -uselsss
    #    print(packet)
    #if packet.packetId != 9: 
    #    print("Received:", packet)
    #    print()