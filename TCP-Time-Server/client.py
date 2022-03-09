import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(("127.0.0.1",6666))

msg = "Hi Server Set My Time".encode("UTF-8")

client.send(msg)

time = client.recv(1024)

time = time.decode("UTF-8")

print(f"The Time Now Is {time}")

client.close()
