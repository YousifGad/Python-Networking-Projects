import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # IPV4 , UDP

sock.bind(("127.0.0.1",5555))

print("[Server Up...]")

while True:
    Rdata , addr = sock.recvfrom(1030)

    Rdata = Rdata.decode("UTF-8")

    print(f"Message Recived From {addr[0]} On Port {addr[1]} : \n => {Rdata}")
    print("-" * 50)

    msg = input("Type Your Message: ")

    if msg.lower() == "q" or msg.lower() == "quit":
        break

    else:
        Sdata = msg.encode("UTF-8")
        
        sock.sendto(Sdata,addr)

        print("[Message Sent!]")
        print("-" * 50)
