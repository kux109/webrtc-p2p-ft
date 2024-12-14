import pyshark

def calculate_webrtc_packet_loss(pcap_file):
    try:
        capture = pyshark.FileCapture(pcap_file, display_filter='stun')
        print(f"Pcap file {pcap_file} opened successfully")
    except Exception as e:
        print(f"Error opening pcap file: {e}")
        return 0

    sent_packets = 0
    received_packets = 0
    packet_count = 0

    try:
        for packet in capture:
            packet_count += 1
            print(f"Processing packet {packet_count}...")  # Debug statement to confirm loop entry
            if hasattr(packet, 'stun'):
                stun_layer = packet.stun
                if hasattr(stun_layer, 'type'):
                    stun_type = stun_layer.type
                    if stun_type == '0x0001':  # Binding Request
                        sent_packets += 1
                        print(f"STUN request found: {sent_packets} total requests")
                    elif stun_type == '0x0101':  # Binding Success Response
                        received_packets += 1
                        print(f"STUN response found: {received_packets} total responses")
                else:
                    print("STUN layer missing type")  # Debug print
            else:
                print(f"No STUN layer found in packet {packet_count}")  # Debug print
    except Exception as e:
        print(f"Error processing packets: {e}")

    capture.close()
    loss_rate = ((sent_packets - received_packets) / sent_packets) * 100 if sent_packets > 0 else 0
    print(f"Sent packets: {sent_packets}, Received packets: {received_packets}, Loss rate: {loss_rate:.2f}%")
    return loss_rate

loss_webrtc = calculate_webrtc_packet_loss('webrtc_100mb.pcapng')
print(f"WebRTC Packet Loss Rate: {loss_webrtc:.2f}%")