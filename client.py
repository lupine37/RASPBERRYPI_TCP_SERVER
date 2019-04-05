import socket


def MasterCard_entry(n):
    lines = []

    MASTERCARD_ID = n+'\n'
    f = open('/home/pi/Desktop/door_lock_project/MASTERCARD.txt', 'r')

    for line in f:
        lines.append(line)
        if (MASTERCARD_ID == line):
            print("WELCOME TO MASTERMODE")
            print("please insert a card to add or remove")
    f.close()


def rfidAccess(n, d):
    lines = []

    rfid_ID = " "
    rfid_ID = n+'\n'
    f = open('/home/pi/Desktop/door_lock_project/rfidData.txt', 'r')

    for line in f:
        lines.append(line)
    f.close()
    for line in lines:
        if rfid_ID == line:
            d = d + 1
            return d


def Main():
    host = '192.168.1.105'
    port = 8888
    Access = "<GRANTED>"
    Denied = "<DENIED>"
    count = 0

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    while True:
        data = s.recv(1024).decode('utf-8')
        if not data:
            break
        if (data != " "):
            print(data)
            count = rfidAccess(data, count)
            print(count)
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
