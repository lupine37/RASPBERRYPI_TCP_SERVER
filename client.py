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


def select_sqlData(n):
    data = ()
    wronglist = (0, 0, 0, 0)
    c.execute("SELECT * FROM rfidData WHERE UID_NO = :uid_no", {'uid_no': n})
    data = c.fetchone()
    if data:
        return(data)
    else:
        return(wronglist)


def Add_sqlData(n):
    c.execute("SELECT UID_NO FROM rfidData WHERE UID_NO = :uid_no",
              {'uid_no': n})
    data = c.fetchone()
    for uid_no in data:
        if uid_no == n:
            print("ALREADY EXIST")
        else:
            name = input("NAME: ")
            house_no = input("HOUSE NO: ")

            with conn:
                c.execute("""INSERT INTO rfidData VALUES
                           (:house_no, :name, :uid_no,:card_type)""",
                          {'house_no': house_no, 'name': name,
                           'uid_no': n, 'card_type': 'ORD'})


def Remove_sqlData(n):
    c.execute("SELECT UID_NO FROM rfidData WHERE UID_NO = :uid_no",
              {'uid_no': n})
    data = c.fetchone()
    for uid_no in data:
        if uid_no == n:
            with conn:
                c.execute("""DELETE FROM rfidData WHERE UID_no = :uid_no""",
                          {'uid_no': n})


def Mastermode():
    cardUID = ""
    response = input("ARE YOU SURE FOR MASTERMODE?(yes/no) ")
    if response == 'yes':
        while True:
            response = input("TO ADD OR REMOVE A CARD OR EXIT: ")
            if response == 'ADD':
                print("PLACE YOUR CARD")
                while True:
                    cardUID = s.recv(1024).decode('utf-8')
                    if not cardUID:
                        break
                    if cardUID != " ":
                        print(cardUID)
                        Add_sqlData(cardUID)
                        break
            elif response == 'REMOVE':
                print("PLACE YOUR CARD")
                while True:
                    cardUID = s.recv(1024).decode('utf-8')
                    if not cardUID:
                        break
                    if cardUID != " ":
                        print(cardUID)
                        Remove_sqlData(cardUID)
                        break
            elif response == 'EXIT':
                break
    elif response == 'no':
        print("ok")


def Main():
    count = 0
    while True:
        clientData = s.recv(1024).decode('utf-8')
        if not clientData:
            break
        if (clientData != " "):
            print(clientData)
            sqldata = select_sqlData(clientData)
            try:
                dataInfo = rfidUID(sqldata)
            except Exception:
                print("wrong card")
            print(dataInfo.name)
            if dataInfo.uid_no == clientData:
                if dataInfo.card_type == "MASTERCARD":
                    Mastermode()
                elif dataInfo.card_type == "ORD":
                    count = count + 1
            else:
                count = count - 1
            if count == 3:
                print(Access)
                s.send(Access.encode('utf-8'))
                count = 0
            elif count == -3:
                print(Denied)
                s.send(Denied.encode('utf-8'))
                count = 0
    s.close()


if __name__ == '__main__':
    Main()
