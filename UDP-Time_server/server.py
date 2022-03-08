import socket
from datetime import datetime

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

sock.bind(("127.0.0.1",5555))

print("[Server Up...]")

Rdata , addr = sock.recvfrom(1030)

Rdata = Rdata.decode("UTF-8")

print(f"Request From {addr[0]} On Port {addr[1]}: \n => {Rdata}")

time = str(datetime.now())

Sdata = time.encode("UTF-8")

sock.sendto(Sdata,addr)

print("[Server Responsed Successfully...]")