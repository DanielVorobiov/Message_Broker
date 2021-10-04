from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

HOST = "localhost"
PORT = 8080

topic_db = {}
subscribers_db = {}


def senders(data):
    topic = data['topic']
    message = data['message']
    if topic not in topic_db:
        topic_db[topic] = message
        subscribers_db[topic] = None
    topic_db[topic] = message
    print(topic_db)
    print(subscribers_db)
    sender_data = {topic: topic_db[topic]}

    if subscribers_db[topic] != None:
        subscribers = subscribers_db[topic]
        print(subscribers)
        for subscriber in subscribers:
            with xmlrpc.client.ServerProxy(f"http://{subscriber[0]}:{subscriber[1]}/") as proxy:
                proxy.recieve_message(data)


def recievers():
    if len(topic_db) == 0:
        reciever_data = {"topics": "There are no topics yet."}
    else:
        reciever_data = {'topics': list(topic_db.keys())}
    return reciever_data


def subscribe(addr, data):
    topics = data['topics']
    for topic in topics:
        if subscribers_db[topic] == None:
            subscribers_db[topic] = []
        subscribers_db[topic].append(addr)
    print(subscribers_db)


server = SimpleXMLRPCServer((HOST, PORT), allow_none=True)
print("Listening on port 8080...")
server.register_function(senders, "senders")
server.register_function(recievers, "recievers")
server.register_function(subscribe, "subscribe")
server.serve_forever()
