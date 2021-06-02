#! /usr/bin/env python3

"""This script monitors a UDP port for F1 2019 telemetry packets and prints useful info upon reception."""

import argparse
import sys
import socket
import threading
import logging
import selectors
import math

from f1_2020_telemetry.cli.threading_utils import WaitConsoleThread, Barrier
from f1_2020_telemetry.packets import PacketID, unpack_udp_packet


class PacketMonitorThread(threading.Thread):
    """The PacketMonitorThread receives incoming telemetry packets via the network and shows interesting information."""

    def __init__(self, udp_port):
        super().__init__(name="monitor")
        self._udp_port = udp_port
        self._socketpair = socket.socketpair()

        self._current_frame = None
        self._current_frame_data = {}

    def close(self):
        for sock in self._socketpair:
            sock.close()

    def run(self):
        """Receive incoming packets and print info about them.

        This method runs in its own thread.
        """

        udp_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM
        )

        
        if sys.platform in ["linux", "win32"]:
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Accept UDP packets from any host.
        address = ("", self._udp_port)
        udp_socket.bind(address)

        selector = selectors.DefaultSelector()

        key_udp_socket = selector.register(udp_socket, selectors.EVENT_READ)
        key_socketpair = selector.register(
            self._socketpair[0], selectors.EVENT_READ
        )

        logging.info(
            "Monitor thread started, reading UDP packets from port %d",
            self._udp_port,
        )

        quitflag = False
        while not quitflag:
            for (key, events) in selector.select():
                if key == key_udp_socket:
                    # All telemetry UDP packets fit in 2048 bytes with room to spare.
                    udp_packet = udp_socket.recv(2048)
                    packet = unpack_udp_packet(udp_packet)
                    self.process(packet)
                elif key == key_socketpair:
                    quitflag = True

        self.report()

        selector.close()
        udp_socket.close()
        for sock in self._socketpair:
            sock.close()

        logging.info("Monitor thread stopped.")

    def process(self, packet):

        if packet.header.frameIdentifier != self._current_frame:
            self.report()
            self._current_frame = packet.header.frameIdentifier
            self._current_frame_data = {}

        self._current_frame_data[PacketID(packet.header.packetId)] = packet

    def report(self):
        if self._current_frame is None:
            return

        any_packet = next(iter(self._current_frame_data.values()))

        player_car = any_packet.header.playerCarIndex

        #track id , -1 for unknown, 0-21 for tracks, see appendix
        try:
            trackid = (
                self._current_frame_data[PacketID.SESSION]
                #.lapData[player_car]
                #.PacketSessionData.weather
                #.s
                .trackId
            )
        except:
            trackid = "none"
        if trackid is "none":
            return

        
        #Formulaid , 0 = F1 Modern, 1 = F1 Classic, 2 = F2, 3 = F1 Generic ,  4 nothing
        try:
            formulaid = (
                self._current_frame_data[PacketID.SESSION]
                .Formula
            )
        except:
            formulaid = 4
        #Weather Weather - 0 = clear, 1 = light cloud, 2 = overcast 3 = light rain, 4 = heavy rain, 5 = storm , 6 nothing
        try:
            weatherid = (
                self._current_frame_data[PacketID.SESSION]
                .weather
            )
        except:
            weatherid = 6
        #carId
        try:
            carid = (
                self._current_frame_data[PacketID.SESSION]
                .Formula
            )
        except:
            carid = 4
        #track*C
        try:
            trackTemp = (
                self._current_frame_data[PacketID.SESSION]
                .trackTemperature
            )
        except:
            trackTemp = 4
        #air *c
        try:
            airTemp = (
                self._current_frame_data[PacketID.SESSION]
                .airTemperature
            )
        except:
            airTemp = 4
        logging.info("frame %6d playercar %s trackid %s formulaid %s weatherid %s carid %s trackTemp %s airTemp %s", self._current_frame, player_car, trackid, formulaid, weatherid, carid, trackTemp, airTemp)

    def request_quit(self):
        """Request termination of the PacketMonitorThread.

        Called from the main thread to request that we quit.
        """
        self._socketpair[1].send(b"\x00")


def main():
    """Record incoming telemetry data until the user presses enter."""

    # Configure logging.

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-23s | %(threadName)-10s | %(levelname)-5s | %(message)s",
    )
    logging.Formatter.default_msec_format = "%s.%03d"

    # Parse command line arguments.

    parser = argparse.ArgumentParser(
        description="Monitor UDP port for incoming F1 2019 telemetry data and print information."
    )

    parser.add_argument(
        "-p",
        "--port",
        default=20777,
        type=int,
        help="UDP port to listen to (default: 20777)",
        dest="port",
    )

    args = parser.parse_args()

    # Start recorder thread first, then receiver thread.

    quit_barrier = Barrier()

    monitor_thread = PacketMonitorThread(args.port)
    monitor_thread.start()

    wait_console_thread = WaitConsoleThread(quit_barrier)
    wait_console_thread.start()

    # Monitor and wait_console threads are now active. Run until we're asked to quit.

    quit_barrier.wait()

    # Stop threads.

    wait_console_thread.request_quit()
    wait_console_thread.join()
    wait_console_thread.close_conn()

    monitor_thread.request_quit()
    monitor_thread.join()
    monitor_thread.close()

    # All done.

    logging.info("All done.")


if __name__ == "__main__":
    main()

"""
Listen to telemetry packets and print them to standard output
"""
"""
import socket
import struct

from f1_2020_telemetry.packets import unpack_udp_packet

udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_socket.bind(("", 20777))
#while True:
#    udp_packet = udp_socket.recv(2048)
#    packet = unpack_udp_packet(udp_packet)
    #print("Received:", packet)
    #print()
#Packet Header

    # decode the header
    packetFormat, = struct.unpack('<H', header[:2])
    gameMajorVersion, = struct.unpack('<B', header[2:3])
    gameMinorVersion, = struct.unpack('<B', header[3:4])
    packetVersion, = struct.unpack('<B', header[4:5])
    packetId, = struct.unpack('<B', header[5:6])
    sessionUID, = struct.unpack('<Q', header[6:14])
    sessionTime, = struct.unpack('<f', header[14:18])
    frameIdentifier, = struct.unpack('<B', header[18:19])
    playerCarIndex, = struct.unpack('<B', header[19:20])

    print (f'as')

    if (packetId == 6):
        fmt = "<HfffbH"
        size = struct.calcsize(fmt)
        d = struct.unpack("<HfffbH", telemetry[:size])
        print (f'Data {d}')
"""

"""
struct PacketHeader{
    uint16    m_packetFormat;             # 2020
    uint8     m_gameMajorVersion;         # Game major version - "X.00"
    uint8     m_gameMinorVersion;         # Game minor version - "1.XX"
    uint8     m_packetVersion;            # Version of this packet type, all start from 1
    uint8     m_packetId;                 # Identifier for the packet type, see below
    uint64    m_sessionUID;               # Unique identifier for the session
    float     m_sessionTime;              # Session timestamp
    uint32    m_frameIdentifier;          # Identifier for the frame the data was retrieved on
    uint8     m_playerCarIndex;           # Index of player's car in the array
    
   # ADDED IN BETA 2: 
    uint8     m_secondaryPlayerCarIndex;  # Index of secondary player's car in the array (splitscreen)
                                          # 255 if no second player
}

#Packet IDs
Motion , 0  	        #Contains all motion data for player’s car – only sent while player is in control
Session, 1              #Data about the session – track, time left
Lap Data, 2             #Data about all the lap times of cars in the session
Event, 3                #Various notable events that happen during a session
Participants, 4         #List of participants in the session, mostly relevant for multiplayer
Car Setups, 5           #Packet detailing car setups for cars in the race
Car Telemetry, 6        #Telemetry data for all cars
Car Status, 7           #Status data for all cars such as damage
Final Classification, 8 #Final classification confirmation at the end of a race
Lobby Info, 9           #Information about players in a multiplayer lobby



#Session Packet
#The session packet includes details about the current session in progress.

#Frequency: 2 per second
#Size: 251 bytes (Packet size updated in Beta 3)
#Version: 1

struct MarshalZone
{
    float  m_zoneStart;   # Fraction (0..1) of way through the lap the marshal zone starts
    int8   m_zoneFlag;    # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
}

struct WeatherForecastSample
{
    uint8     m_sessionType;                     # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P, 5 = Q1
                                                 # 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ, 10 = R, 11 = R2
                                                 # 12 = Time Trial
    uint8     m_timeOffset;                      # Time in minutes the forecast is for
    uint8     m_weather;                         # Weather - 0 = clear, 1 = light cloud, 2 = overcast
                                                 # 3 = light rain, 4 = heavy rain, 5 = storm
    int8      m_trackTemperature;                # Track temp. in degrees celsius
    int8      m_airTemperature;                  # Air temp. in degrees celsius
}

struct PacketSessionData
{
    PacketHeader    m_header;                    # Header

    uint8           m_weather;                   # Weather - 0 = clear, 1 = light cloud, 2 = overcast
                                                 # 3 = light rain, 4 = heavy rain, 5 = storm
    int8	    m_trackTemperature;          # Track temp. in degrees celsius
    int8	    m_airTemperature;            # Air temp. in degrees celsius
    uint8           m_totalLaps;                 # Total number of laps in this race
    uint16          m_trackLength;               # Track length in metres
    uint8           m_sessionType;               # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P
                                                 # 5 = Q1, 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ
                                                 # 10 = R, 11 = R2, 12 = Time Trial
    int8            m_trackId;                   # -1 for unknown, 0-21 for tracks, see appendix
    uint8           m_formula;                   # Formula, 0 = F1 Modern, 1 = F1 Classic, 2 = F2,
                                                 # 3 = F1 Generic
    uint16          m_sessionTimeLeft;           # Time left in session in seconds
    uint16          m_sessionDuration;           # Session duration in seconds
    uint8           m_pitSpeedLimit;             # Pit speed limit in kilometres per hour
    uint8           m_gamePaused;                # Whether the game is paused
    uint8           m_isSpectating;              # Whether the player is spectating
    uint8           m_spectatorCarIndex;         # Index of the car being spectated
    uint8           m_sliProNativeSupport;	 # SLI Pro support, 0 = inactive, 1 = active
    uint8           m_numMarshalZones;           # Number of marshal zones to follow
    MarshalZone     m_marshalZones[21];          # List of marshal zones – max 21
    uint8           m_safetyCarStatus;           # 0 = no safety car, 1 = full safety car
                                                 # 2 = virtual safety car
    uint8           m_networkGame;               # 0 = offline, 1 = online
    uint8           m_numWeatherForecastSamples; # Number of weather samples to follow
    WeatherForecastSample m_weatherForecastSamples[20];   # Array of weather forecast samples
}









"""
