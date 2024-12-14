import pyshark

def calculate_webrtc_rtt(pcap_file):
    capture = pyshark.FileCapture(pcap_file, display_filter='stun')
    request_times = {}
    rtts = []

    for packet in capture:
        print("Processing packet...")  # Debug print
        if hasattr(packet, 'stun'):
            print("STUN layer found")  # Debug print
            stun_layer = packet.stun
            print(stun_layer)  # Print the entire stun layer for inspection
            print(stun_layer.field_names)  # Print all available field names in the stun layer
            for field in stun_layer.field_names:
                print(f"{field}: {getattr(stun_layer, field)}")  # Print each field and its value
            if hasattr(stun_layer, 'type') and hasattr(stun_layer, 'id'):
                message_type = stun_layer.type
                transaction_id = stun_layer.id
                print(f"Transaction ID: {transaction_id}, Message Type: {message_type}")  # Debug print

                if '0x0001' in message_type:  # Binding Request
                    request_times[transaction_id] = float(packet.sniff_time.timestamp())
                    print(f"Request Time: {request_times[transaction_id]} for Transaction ID: {transaction_id}")  # Debug print
                elif '0x0101' in message_type and transaction_id in request_times:  # Binding Success Response
                    response_time = float(packet.sniff_time.timestamp())
                    request_time = request_times.pop(transaction_id)
                    rtts.append(response_time - request_time)
                    print(f"RTT: {response_time - request_time} for Transaction ID: {transaction_id}")  # Debug print
            else:
                print("STUN layer missing type or id")  # Debug print
        else:
            print("No STUN layer found")  # Debug print

    capture.close()
    return rtts

webrtc_rtt = calculate_webrtc_rtt('webrtc_100mb.pcapng')
print(f"WebRTC RTTs: {webrtc_rtt}")
print(f"Average RTT: {sum(webrtc_rtt) / len(webrtc_rtt) if webrtc_rtt else 'No RTT data'} ms")