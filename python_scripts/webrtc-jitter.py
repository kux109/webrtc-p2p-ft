import pyshark

def calculate_webrtc_jitter(pcap_file):
    try:
        capture = pyshark.FileCapture(pcap_file, display_filter='stun')
        print(f"Pcap file {pcap_file} opened successfully")
    except Exception as e:
        print(f"Error opening pcap file: {e}")
        return []

    arrival_times = []
    packet_count = 0

    try:
        for packet in capture:
            packet_count += 1
            print(f"Processing packet {packet_count}...")  # Debug statement to confirm loop entry
            arrival_times.append(float(packet.sniff_time.timestamp()))
    except Exception as e:
        print(f"Error processing packets: {e}")

    capture.close()
    jitters = [abs(arrival_times[i] - arrival_times[i - 1]) for i in range(1, len(arrival_times))]
    return jitters

jitter_webrtc = calculate_webrtc_jitter('webrtc_100mb.pcapng')
print(f"WebRTC Jitter Values: {jitter_webrtc}")