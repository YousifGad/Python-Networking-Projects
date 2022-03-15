import socket
import threading
from getpass import getpass

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("127.0.0.1",5555))

nickname = input("Choose a nickname: ")
if nickname == "admin":
	password = getpass("Enter the admin's password: ")

stop = False

def receive():
	while True:
		global stop
		if stop:
			break

		try:
			message = client.recv(1024).decode("UTF-8")
			if message == "Nickname:":
				client.send(nickname.encode("UTF-8"))

				next_message = client.recv(1024).decode("UTF-8")
				if next_message == "PASS":
					client.send(password.encode("UTF-8"))
					if client.recv(1024).decode("UTF-8") == "REFUSE":
						print("Wrong password!")
						stop = True

				elif next_message == "BAN":
					print("Connection refused because of ban!")
					stop = True
				else:
					print(next_message)

			else:
				print(message)

		except:
			stop = True


def write():
	while True:
		global stop
		if stop:
			break
				
		message = f"{nickname}: {input()}"
		if message[len(nickname)+2:].startswith("/"):
			
			if message[len(nickname)+2:].startswith("/kick"):
				client.send(f"KICK {message[len(nickname)+2+6:]}".encode("UTF-8"))

			elif message[len(nickname)+2:].startswith("/ban"):
				client.send(f"BAN {message[len(nickname)+2+5:]}".encode("UTF-8"))

			elif message[len(nickname)+2:].startswith("/clear"):
				client.send("CLEAR".encode("UTF-8"))
			
			else:
				print("Enter a valid command!")
			
		elif message[len(nickname)+2:].lower() == "quit":
			client.send("QUIT".encode("UTF-8"))
			client.close()
			stop = True

		else:
			if stop == False:
				client.send(message.encode("UTF-8"))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
