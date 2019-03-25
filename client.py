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


def rfidAccess(n):
    lines = []

    rfid_ID = n+'\n'
    f = open('/home/pi/Desktop/door_lock_project/rfidData.txt', 'r')

    for line in f:
        lines.append(line)
        if (rfid_ID == line):
            return 1


def Main():
    host = '192.168.1.105'
    port = 8888
    Access = "<ON>"
    Denied = "<OFF>"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    while True:
        data = s.recv(1024).decode('utf-8')
        if not data:
            break
        if (data != " "):
            print(data)
            output = rfidAccess(data)
            if (output == 1):
                print(output)
                print(Access)
                s.send(Access.encode('utf-8'))
            else:
                print(Denied)
                s.send(Denied.encode('utf-8'))
    s.close()


if __name__ == '__main__':
    Main()
