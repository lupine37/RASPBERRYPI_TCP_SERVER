import socket
import sqlite3

host = '192.168.1.171'
port = 8888
id_no = "<ID>"
Access = "<GRANTED>"
Denied = "<DENIED>"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
print("listening to client....")
con, addr = s.accept()
print("Connected")
conn = sqlite3.connect("rfidData.db")
c = conn.cursor()


class rfidUID:
    list = ()

    def __init__(self, list):
        self.house_no = list[0]
        self.name = list[1]
        self.uid_no = list[2]
        self.card_type = list[3]
        self.finger_no = list[4]


def select_sqlData(n):
    data = ()
    wronglist = (0, 0, 0, 0, 0)
    c.execute("SELECT * FROM rfidData WHERE UID_NO = :uid_no", {'uid_no': n})
    data = c.fetchone()
    if data:
        return(data)
    else:
        return(wronglist)


def EnrollFingerID(n):
    con.send("<Enroll>".encode('utf-8'))
    while True:
        data = con.recv(1024).decode('utf-8')
        if not data:
            break
        if data != " ":
            print(data)
            if data == 'idNo':
                con.send(n.encode('utf-8'))
            elif data == "Stored":
                return ("#"+n)
                break
            elif data == 'break':
                return 0
                break


def Add_sqlData(n):
    list = []
    idNo = 0
    n = n.replace(" ", "")
    for line in n:
        list.append(line)
    n = ''.join(list[0:8])
    uid_no = ""
    c.execute("SELECT UID_NO FROM rfidData WHERE CARD_TYPE = 'MASTERCARD'")
    cardInfo = c.fetchone()
    c.execute("SELECT UID_NO FROM rfidData WHERE UID_NO = :uid_no",
              {'uid_no': n})
    data = c.fetchone()
    try:
        for raw in cardInfo:
            MasterCard = raw
        for raw in data:
            uid_no = raw
    except Exception:
        pass
    finally:
        if n == MasterCard:
            print("Try Again")
        else:
            if uid_no == n:
                print("ALREADY EXIST")
            else:
                name = input("NAME: ")
                house_no = input("HOUSE NO: ")
                idNo = EnrollFingerID(house_no)
                if idNo != 0:
                    print(idNo)
                    with conn:
                        c.execute("""INSERT INTO rfidData VALUES
                                  (:house_no, :name, :uid_no, :card_type,
                                   :idNo)""",
                                  {'house_no': house_no, 'name': name,
                                   'uid_no': n, 'card_type': 'ORD',
                                   'idNo': idNo})
                    print("ADDED")


def Remove_sqlData(n):
    list = []
    n = n.replace(" ", "")
    for line in n:
        list.append(line)
    n = ''.join(list[0:8])
    uid_no = ""
    c.execute("SELECT UID_NO FROM rfidData WHERE CARD_TYPE = 'MASTERCARD'")
    cardInfo = c.fetchone()
    c.execute("SELECT UID_NO FROM rfidData WHERE UID_NO = :uid_no",
              {'uid_no': n})
    data = c.fetchone()
    try:
        for raw in cardInfo:
            MasterCard = raw
        for raw in data:
            uid_no = raw
    except TypeError:
        print("card Does Not Exist")
    finally:
        if n == MasterCard:
            print("Try Again")
        else:
            if uid_no == n:
                with conn:
                    c.execute("""DELETE FROM rfidData WHERE UID_NO =
                                  :uid_no""",
                              {'uid_no': n})


def Mastermode():
    while True:
        response = input("TO ADD OR REMOVE A CARD OR EXIT: ")
        if response == 'ADD':
            print("PLACE YOUR CARD")
            while True:
                cardUID = con.recv(1024).decode('utf-8')
                if not cardUID:
                    break
                if cardUID != " ":
                    print(cardUID)
                    Add_sqlData(cardUID)
                    break
        elif response == 'REMOVE':
            print("PLACE YOUR CARD")
            while True:
                cardUID = con.recv(1024).decode('utf-8')
                if not cardUID:
                    break
                if cardUID != " ":
                    print("Remove "+cardUID)
                    Remove_sqlData(cardUID)
                    break
        elif response == 'EXIT':
            break


def Main():
    count = 0
    id_count = 0
    while True:
        clientData = con.recv(1024).decode('utf-8')
        if not clientData:
            break
        if (clientData != " "):
            print(clientData)
            sqldata = select_sqlData(clientData)
            try:
                dataInfo = rfidUID(sqldata)
            except Exception:
                print("wrong card")
            except UnboundLocalError:
                pass
            print(dataInfo.name)
            if dataInfo.uid_no == clientData:
                if dataInfo.card_type == "MASTERCARD":
                    clientData = ""
                    Mastermode()
                elif dataInfo.card_type == "ORD":
                    count = count + 1
            else:
                count = count - 1
            if count == 3:
                print(Access)
                con.send(id_no.encode('utf-8'))
                while True:
                    data = con.recv(1024).decode('utf-8')
                    if not data:
                        break
                    if data != " ":
                        print(data)
                        if dataInfo.finger_no == data:
                            con.send(Access.encode('utf-8'))
                            break
                        elif data == 'break':
                            break
                        else:
                            id_count = id_count + 1
                count = 0
            elif count == -3:
                print(Denied)
                con.send(Denied.encode('utf-8'))
                count = 0
            elif id_count == 3:
                print(Denied)
                con.send(Denied.encode('utf-8'))
                id_count = 0
    con.close()


if __name__ == '__main__':
    Main()
