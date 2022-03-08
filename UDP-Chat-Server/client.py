import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # IPV4 , UDP

while True:
    msg = input("Type Your Message: ")

    if msg.lower() == "q" or msg.lower() == "quit":
        break

    else:
        Sdata = msg.encode("UTF-8")

        sock.sendto(Sdata,("127.0.0.1",5555))

        print("[Waiting For Responce...]")
        print("-" * 50)

        Rdata , addr = sock.recvfrom(1030)

        Rdata = Rdata.decode("UTF-8")

        print(f"Message Recived From {addr[0]} On Port {addr[1]} : \n => {Rdata}")
        print("-" * 50)
