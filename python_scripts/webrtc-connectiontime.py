import pyshark

def calculate_webrtc_connection_time(pcap_file):
    try:
        capture = pyshark.FileCapture(pcap_file, display_filter='stun')
        print(f"Pcap file {pcap_file} opened successfully")
    except Exception as e:
        print(f"Error opening pcap file: {e}")
        return None

    start_time = None
    end_time = None
    packet_count = 0

    try:
        for packet in capture:
            packet_count += 1
            print(f"Processing packet {packet_count}...")  # Debug statement to confirm loop entry
            if hasattr(packet, 'stun'):
                stun_layer = packet.stun
                if hasattr(stun_layer, 'type'):
                    stun_type = stun_layer.type
                    if stun_type == '0x0001' and not start_time:  # Binding Request
                        start_time = float(packet.sniff_time.timestamp())
                        print(f"Start time recorded: {start_time}")
                    elif stun_type == '0x0101':  # Binding Success Response
                        end_time = float(packet.sniff_time.timestamp())
                        print(f"End time recorded: {end_time}")
                        break
                else:
                    print("STUN layer missing type")  # Debug print
            else:
                print(f"No STUN layer found in packet {packet_count}")  # Debug print
    except Exception as e:
        print(f"Error processing packets: {e}")

    capture.close()
    return end_time - start_time if start_time and end_time else None

conn_time_webrtc = calculate_webrtc_connection_time('webrtc_100mb.pcapng')
print(f"WebRTC Connection Establishment Time: {conn_time_webrtc:.2f} seconds")