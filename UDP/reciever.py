import socket
import json

HOST = "localhost"
PORT = 8080

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
connect_message = {"connect_message": "Reciever"}
connect_message = json.dumps(connect_message)
connect_message = connect_message.encode()
socket.sendto(connect_message, (HOST, PORT))
selected_topics = []
while True:
    broker_data, addr = socket.recvfrom(1024)
    if not broker_data:
        break
    broker_data.decode()
    broker_data = json.loads(broker_data)
    if 'topics' in broker_data:
        topics = broker_data['topics']
        if topics == 'There are no topics yet.':
            print(topics)
            break

        if len(selected_topics) > 0:
            continue
        else:
            print("Available topics: ")
            for topic in topics:
                print(topic)
            selected_topics = list(input("Select a topic: ").split(', '))
            print(selected_topics)
            data = {'topics': selected_topics}
            data = json.dumps(data)
            data = data.encode()
            socket.sendto(data, (HOST, PORT))
    else:

        for k, v in broker_data.items():
            print(v)


socket.close()
