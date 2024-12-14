import pyshark

print("Starting WebRTC Latency Calculator script")  # Debug statement to confirm script start

pcap_file = 'webrtc_100mb.pcapng'
print(f"Opening pcap file: {pcap_file}")
try:
    capture = pyshark.FileCapture(pcap_file, display_filter='stun')
    print("Pcap file opened successfully")
except Exception as e:
    print(f"Error opening pcap file: {e}")
    capture = None

if capture is not None:
    request_timestamps = {}
    latencies = []
    packet_count = 0
    print(f"Processing {pcap_file}...")

    try:
        for packet in capture:
            packet_count += 1
            print(f"Processing packet {packet_count}...")  # Debug statement to confirm loop entry
            if hasattr(packet, 'stun'):
                stun_layer = packet.stun
                print("STUN layer found")
                if hasattr(stun_layer, 'type') and hasattr(stun_layer, 'id'):
                    stun_type = stun_layer.type
                    transaction_id = stun_layer.id
                    timestamp = float(packet.sniff_timestamp)
                    print(f"STUN type: {stun_type}, Transaction ID: {transaction_id}, Timestamp: {timestamp}")

                    if stun_type == '0x0001':  # Binding Request
                        request_timestamps[transaction_id] = timestamp
                        print(f"STUN request recorded: {transaction_id} at {timestamp}")
                    elif stun_type == '0x0101':  # Binding Success Response
                        if transaction_id in request_timestamps:
                            request_time = request_timestamps.pop(transaction_id)
                            latency = (timestamp - request_time) * 1000  # Convert to milliseconds
                            latencies.append(latency)
                            print(f"STUN response recorded: {transaction_id} at {timestamp}, Latency: {latency} ms")
                        else:
                            print(f"Transaction ID {transaction_id} not found in request_timestamps")
                    else:
                        print(f"Unknown STUN type: {stun_type}")
                else:
                    print("STUN layer missing type or id")  # Debug print
            else:
                print(f"No STUN layer found in packet {packet_count}")  # Debug print
    except Exception as e:
        print(f"Error processing packets: {e}")

    capture.close()
    print(f"WebRTC Latencies: {latencies}")
    print(f"Average Latency: {sum(latencies) / len(latencies) if latencies else 'No Latency data'} ms")
else:
    print("Failed to process pcap file")