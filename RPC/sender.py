import xmlrpc.client

with xmlrpc.client.ServerProxy("http://localhost:8080/") as proxy:
    topic = input("Topic: ")
    message = input("Message: ")
    data = {'topic': topic, 'message': message}
    proxy.senders(data)
