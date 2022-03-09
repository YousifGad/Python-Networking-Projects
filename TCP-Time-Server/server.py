import socket
from datetime import datetime

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(("127.0.0.1",6666))

server.listen(5)

print("[Server Up...]")

while True:
	client , addr = server.accept()

	msg = client.recv(1024)

	msg = msg.decode("UTF-8")

	print(f"Client {addr[0]} On Port {addr[1]} Message: \n => {msg}")

	time = str(datetime.now().time()).encode("UTF-8")

	client.send(time)

	print("[Server Responsed!]")

	print("-" * 50)

	client.close()
