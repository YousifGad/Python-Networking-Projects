import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

Sdata = "Hey Server! Set My Time"

Sdata = Sdata.encode("UTF-8")

sock.sendto(Sdata,("127.0.0.1",5555))

Rdata , addr = sock.recvfrom(1030)

Rdata = Rdata.decode("UTF-8")

print(f"The Time Is {Rdata}")