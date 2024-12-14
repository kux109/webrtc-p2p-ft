import pyshark

def calculate_webrtc_throughput(pcap_file):
    try:
        capture = pyshark.FileCapture(pcap_file)
        packet_count = 0
        total_bytes = 0
        start_time = None
        end_time = None

        for packet in capture:
            packet_count += 1
            print(f"Processing packet {packet_count}...")  # Debug statement to confirm loop entry

            if start_time is None:
                start_time = float(packet.sniff_timestamp)
            end_time = float(packet.sniff_timestamp)

            total_bytes += int(packet.length)
            print(f"Packet length: {packet.length}, Total bytes: {total_bytes}")

        capture.close()

        if start_time is not None and end_time is not None:
            duration = end_time - start_time
            throughput = (total_bytes * 8) / duration  # Throughput in bits per second
            print(f"Duration: {duration} seconds, Total bytes: {total_bytes}, Throughput: {throughput} bps")
        else:
            print("No packets processed, unable to calculate throughput")

    except Exception as e:
        print(f"Error processing pcap file: {e}")

# Example usage
pcap_file = 'webrtc_100mb.pcapng'
calculate_webrtc_throughput(pcap_file)