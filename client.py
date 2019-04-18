import socket
import sqlite3

host = '192.168.1.105'
port = 8888
Access = "<GRANTED>"
Denied = "<DENIED>"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
conn = sqlite3.connect("rfidData.db")
c = conn.cursor()


class rfidUID:
    list = ()

    def __init__(self, list):
        self.house_no = list[0]
        self.name = list[1]
        self.uid_no = list[2]
        self.card_type = list[3]


def sqlData(n):
    data = ()
    wronglist = (0, 0, 0, 0)
    c.execute("SELECT * FROM rfidData WHERE UID_NO = :uid_no", {'uid_no': n})
    data = c.fetchone()
    if data:
        return(data)
    else:
        return(wronglist)


def Main():
    count = 0
    while True:
        clientData = s.recv(1024).decode('utf-8')
        if not clientData:
            break
        if (clientData != " "):
            print(clientData)
            sqldata = sqlData(clientData)
            try:
                dataInfo = rfidUID(sqldata)
            except Exception:
                print("wrong card")
            print(dataInfo.name)
            if dataInfo.uid_no == clientData:
                count = count + 1
            else:
                count = count - 1
            if count == 5:
                print(Access)
                s.send(Access.encode('utf-8'))
                count = 0
            elif count == -5:
                print(Denied)
                s.send(Denied.encode('utf-8'))
                count = 0
    s.close()


if __name__ == '__main__':
    Main()
