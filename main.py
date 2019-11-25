import Server
import dataBase
import io
import PIL.Image
import time
import struct
import binascii
import threading
# import Enrolling_User

message = "kennedy"
template = "<TEMPLATE>"
Access = "<GRANTED>"
Denied = "<DENIED>"
startMarker = '<'
endMarker = '>'
breakTime = False


class rfidUID:
    list = ()

    def __init__(self, list):
        self.house_no = list[0]
        self.name = list[1]
        self.uid_no = list[2]
        self.card_type = list[3]
        self.template = list[4]
        self.entryState = list[5]


def ChangeToString(n):
    s = ''
    if len(str(n)) == 1:
        s = '00' + str(n)
        return(s)
    elif len(str(n)) == 2:
        s = '0' + str(n)
        return(s)
    else:
        return(str(n))

def recvFingerTemplate(data, uid_no):
    lst = []
    lst2 = []
    appendState = False
        # print(data)
    for c in data:
        if c == '[':
            appendState = True
        elif appendState == True:
            if c != ']':
                lst2.append(c)
            else:
                s = ''.join(lst2)
                lst.append(int(s))
                lst2 = []
                appendState = False
    form = 'B' * len(lst)
    temp = struct.pack(form, *lst)
    print(temp)
    dataBase.updateTemplate(uid_no, temp)
    dbData = dataBase.selectTemplate(uid_no)
    # print(binascii.hexlify(dbData[0]))
    print(len(dbData[0]))


def sendFingerTemplate(uid_no, ipAddr):
    dbData = []
    dbList = []
    dbData = dataBase.selectTemplate(uid_no)
    l = len(dbData[0])
    # print(binascii.hexlify(dbData[0]))
    print(l)
    form = 'B' * l
    dbList.extend(struct.unpack(form, dbData[0]))
    Server.sendData(str('<'), ipAddr)
    for hex_v in dbList:
        Server.sendData('[', ipAddr)
        hex_str = ChangeToString(hex_v)
        Server.sendData(str(hex_str), ipAddr)
        Server.sendData(']', ipAddr)
    Server.sendData('>', ipAddr)
    

def Main():
    while True:
        Server.accept_wrapper()
        server_data = Server.recvData()
        if server_data is not None:
            data = server_data[0]
            ipAddr = server_data[1]
            house_no = dataBase.select_house_no(ipAddr[0])
            house_no = house_no[0]
            if house_no == 1:
                sql_data = dataBase.select_sqlMainData(data)
                try:
                    dataInfo = rfidUID(sql_data)
                except Exception:
                    print("wrong card")
                print(dataInfo.name)
                print(bool(dataInfo.entryState))
                if dataInfo.uid_no == data and bool(dataInfo.entryState == False):
                    print(Access)
                    Server.sendData(template, ipAddr)
                    templateState = True
                    startTime = time.time()
                    while True:
                        endTime = time.time()
                        if (endTime - startTime > 15):
                            print("timeout")
                            break
                        else:
                            Server_data = Server.recvData()
                            if Server_data is not None:
                                print(Server_data[0])
                                if Server_data[0] == 'fingerTemplate' and templateState == True:
                                    sendFingerTemplate(dataInfo.uid_no, ipAddr)
                                    templateState = False
                                elif Server_data[0] == 'Match':
                                    Server.sendData(Access, ipAddr)
                                    dataBase.updateEntryState(dataInfo.uid_no, int(not bool(dataInfo.entryState)))
                                    break
                                elif Server_data[0] == 'NoMatch':
                                    Server.sendData(Denied, ipAddr)
                                    break
                                elif Server_data[0] == 'break':
                                    break
                            elif (startTime - endTime) > 5:
                                print("Timeout")
                elif dataInfo.uid_no == data and bool(dataInfo.entryState) == True:
                    Server.sendData(Access, ipAddr)
                    dataBase.updateEntryState(dataInfo.uid_no, int(not bool(dataInfo.entryState)))
                else:
                    print(Denied)
                    Server.sendData(Denied, ipAddr)
            else:
                house_no = 'HOUSE' + str(house_no)
                UIDInfo = dataBase.select_sqlData(house_no)
                print(UIDInfo[0])
                UID_no = UIDInfo[1]
                print(UID_no)
                print(data)
                if data == UID_no:
                    print(Access)
                    Server.sendData(Access, ipAddr)
                else:
                    print(Denied)
                    Server.sendData(Denied, ipAddr)


if __name__ == '__main__':
    Main()
