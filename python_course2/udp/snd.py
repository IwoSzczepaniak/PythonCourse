import socket


def snd(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(bytes(data, 'utf-8'), ('127.0.0.1', 1964))
    s.close()


# end def 

# Send messages 

while (True):
    data = input('>>')
    snd(data)
    if data == 'q': break
# end while
