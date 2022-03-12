import socket
import threading
from pyfiglet import figlet_format
from termcolor import colored


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("127.0.0.1",5555))
server.listen()


print(colored(figlet_format("Server Up"),color="blue"))

clients = []
nicknames = []

def broadcast(message):
	for client in clients:
		client.send(message)


def handle(client):
	while True:
		try:
			mesg = message = client.recv(1024)
			
			if mesg.decode("UTF-8").startswith("KICK"):
			    if nicknames[clients.index(client)] == "admin":
			        name_to_kick = mesg.decode("UTF-8")[5:]
			        kick_user(name_to_kick)
				print(f"{name_to_kick} was kicked!")
			    
			    else: client.send("Commands can be excuted only by admins!".encode("UTF-8"))
			    
			elif mesg.decode("UTF-8").startswith("BAN"):
		        	if nicknames[clients.index(client)] == "admin":
		        		name_to_ban = mesg.decode("UTF-8")[4:]
					kick_user(name_to_ban)
					with open("bans.txt","a") as f:
                        			f.write(f"{name_to_ban}\n")
            				print(f"{name_to_ban} was banned!")

                		else:
					client.send("Commands can be excuted only by admins!".encode("UTF-8"))
                      
			else:
			    broadcast(message.encode("UTF-8"))
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			broadcast(f"{nicknames[index]} left the chat!")
			nicknames.remove(nicknames[index])
			break

			
def receive():
	while True:
		client , addr = server.accept()
		print(f"{addr} connected to the server!")

		client.send("Nickname:".encode("UTF-8"))
		nickname = client.recv(1024).decode("UTF-8")
		
		with open("bans.txt","r") as f:
		    bans = f.readlines()

		if nickname + "\n" in bans:
			client.send("BAN".encode("UTF-8"))
			client.close()
			continue

		if nickname == "admin":
			client.send("PASS".encode("UTF-8"))
			password = client.recv(1024).decode("UTF-8")

			if password != "adminpass":
				client.send("REFUSE".encode("UTF-8"))
				client.close()
				continue

		nicknames.append(nickname)
		clients.append(client)

		print(f"Nickname of the new client is {nickname}")
		broadcast(f"{nickname} joined the chat!".encode("UTF-8"))
		client.send("Connected to the server!".encode("UTF-8"))

		thread = threading.Thread(target=handle, args=(client,))
		thread.start()

		
def kick_user(user):
    if user in nicknames:
        index_to_kick = nicknames.index(user)
        client_to_kick = clients[index_to_kick]
        clients.remove(client_to_kick)
        client_to_kick.send("You have been kicked by an admin!".encode("UTF-8"))
        client_to_kick.close()
        nicknames.remove(user)
        broadcast(f"{user} was kicked by an admin!".encode("UTF-8"))
        

receive()
