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
            msg = client.recv(1024)

            if msg.decode("UTF-8").startswith("KICK"):
                if nicknames[clients.index(client)] == "admin":
                    name_to_kick = msg.decode("UTF-8")[5:]
                    if name_to_kick in nicknames:
                        kick_user(name_to_kick)
                        print(f"{name_to_kick} was kicked!")

                    else:
                        client.send("The name you entered is not in the room!".encode("UTF-8"))

                else:
                    client.send("Commands can be only excuted by the admin!".encode("UTF-8"))

            elif msg.decode("UTF-8").startswith("BAN"):
                if nicknames[clients.index(client)] == "admin":
                    name_to_ban = msg.decode("UTF-8")[4:]
                    if name_to_ban in nicknames:
                        kick_user(name_to_ban)

                        with open("bans.txt","a") as f:
                            f.write(f"{name_to_ban}\n")

                        print(f"{name_to_ban} was banned!")

                    else:
                        client.send("The name you entered is not in the room!".encode("UTF-8"))

                else:
                    client.send("Commands can be only excuted by the admin!".encode("UTF-8"))

            elif msg.decode("UTF-8").startswith("CLEAR"):
                if nicknames[clients.index(client)] == "admin":
                    with open("bans.txt","w") as f:
                        f.write("")
                    print("The bans list was cleared by the admin!")
                    client.send("The bans list was cleared successfully!".encode("UTF-8"))
                else:
                    client.send("Commands can be only excuted by the admin!".encode("UTF-8"))

            elif msg.decode("UTF-8").startswith("QUIT"):
                user_left = nicknames[clients.index(client)]
                nicknames.remove(user_left)
                clients.remove(client)
                client.close()
                broadcast(f"{user_left} left the chat!".encode("UTF-8"))
                print(f"{user_left} left the chat!")

            else:
                broadcast(msg)


        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                broadcast(f"{nicknames[index]} left the chat!".encode("UTF-8"))
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
        client_to_kick.send("You was kicked by an admin!".encode("UTF-8"))
        client_to_kick.close()
        nicknames.remove(user)
        broadcast(f"{user} was kicked by the admin!".encode("UTF-8"))


receive()
