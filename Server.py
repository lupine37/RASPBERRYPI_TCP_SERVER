import socket
import selectors

HOST = '192.168.1.170'
ip1 = '192.168.1.189'
ip2 = '192.168.1.197'
PORT = 8888

sel = selectors.DefaultSelector()


class Message:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr


def accept_wrapper(sock):
    conn, addr = sock.accept()
    print('accepted connection from', addr)
    data = Message(sel, conn, addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def recvData(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            recv_data = recv_data.decode('utf-8')
            if recv_data != " ":
                return(recv_data)

        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()


def ip1Data(key, mask):
    sock = key.fileobj
    data = key.data
    send_data = "hi client 1"
    if mask & selectors.EVENT_WRITE:
        print(repr(send_data), 'to', data.addr)
        sock.send(send_data.encode('utf-8'))


def ip2Data(key, mask):
    sock = key.fileobj
    data = key.data
    send_data = "hi client 2"
    if mask & selectors.EVENT_WRITE:
        print(repr(send_data), 'to', data.addr)
        sock.send(send_data.encode('utf-8'))


lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((HOST, PORT))
lsock.listen()
print('listening on', (HOST, PORT))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)


def runServer():
    recv_data = " "
    try:
        event = sel.select(timeout=None)
        for key, mask in event:
            if key.data is None:
                accept_wrapper(key.fileobj)

    except ConnectionResetError:
        print("one of the clients have shut down!")
