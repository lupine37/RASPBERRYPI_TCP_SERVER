import Server
message = "hi"


def Main():
    recv_data = ""
    while True:
        ipAddr = ()
        Server.accept_wrapper()
        recv_data = Server.recvData()
        if recv_data is not None:
            data = recv_data[0]
            sock = recv_data[1]
            ipAddr = recv_data[2]
            Server.sendData(message, sock, ipAddr)


if __name__ == '__main__':
    Main()
