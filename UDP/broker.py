import socket
import json
import _thread

HOST = "localhost"
PORT = 8080


def senders(addr, thread_name):
    topic = data['topic']
    message = data['message']
    if topic not in topic_db:
        topic_db[topic] = message
        subscribers_db[topic] = False
    topic_db[topic] = message
    print(topic_db)
    print(subscribers_db)
    sender_data = {topic: topic_db[topic]}
    sender_data = json.dumps(sender_data)
    sender_data = sender_data.encode()
    if subscribers_db[topic] != False:
        subscribers = subscribers_db[topic]
        print(subscribers)
        if len(subscribers) == 1:
            socket.sendto(sender_data, subscribers[0])
        else:
            for subscriber in subscribers:
                socket.sendto(sender_data, subscriber)


def recievers(addr, thread_name):
    if len(topic_db) == 0:
        reciever_data = {"topics": "There are no topics yet."}
    else:
        reciever_data = {'topics': list(topic_db.keys())}
    reciever_data = json.dumps(reciever_data)
    reciever_data = reciever_data.encode()
    print(addr)
    socket.sendto(reciever_data, addr)


def subscribe(addr, thread_name):
    topics = data['topics']
    for topic in topics:
        if subscribers_db[topic] == False:
            subscribers_db[topic] = []
            subscribers_db[topic].append(addr)
        else:
            subscribers_db[topic].append(addr)
    print(subscribers_db)


socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind((HOST, PORT))
print("Listening on port 8080...")

topic_db = {}
subscribers_db = {}

while True:
    data, addr = socket.recvfrom(1024)
    if not data:
        break
    data.decode()
    data = json.loads(data)
    if 'connect_message' in data:
        _thread.start_new_thread(recievers, (addr, "Thread "))
    elif 'topics' in data:
        _thread.start_new_thread(subscribe, (addr, "Thread "))
    else:
        print('topic')
        _thread.start_new_thread(senders, (addr, "Thread "))


socket.close()
