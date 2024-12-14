import pyshark

def calculate_webrtc_retransmissions(pcap_file):
    try:
        capture = pyshark.FileCapture(pcap_file, display_filter='rtp')
        print(f"Pcap file {pcap_file} opened successfully")
    except Exception as e:
        print(f"Error opening pcap file: {e}")
        return 0

    retransmissions = 0
    packet_count = 0

    try:
        for packet in capture:
            packet_count += 1
            print(f"Processing packet {packet_count}...")  # Debug statement to confirm loop entry
            if hasattr(packet, 'rtp'):
                rtp_layer = packet.rtp
                if hasattr(rtp_layer, 'marker') and rtp_layer.marker == '1':
                    retransmissions += 1
                    print(f"Retransmission found: {retransmissions} total retransmissions")
            else:
                print(f"No RTP layer found in packet {packet_count}")  # Debug print
    except Exception as e:
        print(f"Error processing packets: {e}")

    capture.close()
    return retransmissions

retrans_webrtc = calculate_webrtc_retransmissions('webrtc_100mb.pcapng')
print(f"WebRTC Retransmissions: {retrans_webrtc}")