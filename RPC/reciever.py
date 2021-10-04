from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

HOST = "localhost"
PORT = 8081


try:
    server = SimpleXMLRPCServer((HOST, PORT), allow_none=True)
except:
    server = SimpleXMLRPCServer((HOST, PORT), allow_none=True)
    PORT += 1

with xmlrpc.client.ServerProxy("http://localhost:8080/") as proxy:
    selected_topics = []
    topics_data = proxy.recievers()

topics = topics_data['topics']
if topics == 'There are no topics yet.':
    print(topics)
else:
    print("Available topics: ")
    for topic in topics:
        print(topic)
    selected_topics = list(input("Select a topic: ").split(', '))
    print(selected_topics)
    data = {'topics': selected_topics}
    proxy.subscribe((HOST, PORT), data)


def recieve_message(data):
    print(data['message'])


print(f"Listening on port {PORT}...")
server.register_function(recieve_message, "recieve_message")
server.serve_forever()
