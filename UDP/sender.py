import socket
import json
HOST = "localhost"
PORT = 8080
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.connect((HOST, PORT))
topic = input("Topic: ")
message = input("Message: ")
data = {'topic': topic, 'message': message}
data = json.dumps(data)
data = data.encode()
socket.send(data)
socket.close()
