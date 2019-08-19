import socket
import selectors

HOST = '192.168.1.170'
PORT = 8888
message = "hi"

sel = selectors.DefaultSelector()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((HOST, PORT))
lsock.listen()
print('listening on', (HOST, PORT))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)


class Message:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr


def accept_wrapper():
    try:
        event = sel.select(timeout=None)
        for key, mask in event:
            sock = key.fileobj
            if key.data is None:
                conn, addr = sock.accept()
                print('accepted connection from', addr)
                data = Message(sel, conn, addr)
                events = selectors.EVENT_READ | selectors.EVENT_WRITE
                sel.register(conn, events, data=data)
    except ConnectionResetError:
        print("one of the clients have shut down!")


def recvData():
    event = sel.select(timeout=None)
    for key, mask in event:
        sock = key.fileobj
        data = key.data
        if key.data is not None:
            if mask & selectors.EVENT_READ:
                recv_data = sock.recv(1024)
                if recv_data:
                    recv_data = recv_data.decode('utf-8')
                    if recv_data != " ":
                        return(recv_data, sock, data.addr)
                else:
                    print('closing connection to', data.addr)
                    sel.unregister(sock)
                    sock.close()


def sendData(recvData, sock, ipAddr):
    if recvData is not None:
        print(ipAddr)
        print(recvData)
        sock.sendto(recvData.encode('utf-8'), ipAddr)
