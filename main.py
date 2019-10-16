import Server
import dataBase
import pdb

message = "hi"
template = "<TEMPLATE>"
Access = "<GRANTED>"
Denied = "<DENIED>"


class rfidUID:
    list = ()

    def __init__(self, list):
        self.name = list[0]
        self.uid_no = list[1]
        self.card_type = list[2]
        self.finger_no = list[3]
        self.house_no = list[4]


def Main():
    while True:
        Server.accept_wrapper()
        server_data = Server.recvData()
        if server_data is not None:
            data = server_data[0]
            ipAddr = server_data[1]
            print(data)
            house_no = dataBase.select_house_no(ipAddr[0])
            house_no = house_no[0]
            if house_no == 1:
                sql_data = dataBase.select_sqlMainData(data)
                try:
                    dataInfo = rfidUID(sql_data)
                except Exception:
                    print("wrong card")
                except UnboundLocalError:
                    pass
                print(dataInfo.name)
                if dataInfo.uid_no == data:
                    countdata = dataBase.select_count(ipAddr[0])
                    for c in countdata:
                        count = c
                    count = count + 1
                    print(count)
                    dataBase.update_count(ipAddr[0], count)
                else:
                    countdata = dataBase.select_count(ipAddr[0])
                    for c in countdata:
                        count = c
                    count = count - 1
                    print(count)
                    dataBase.update_count(ipAddr[0], count)
                if count == 3:
                    print(Access)
                    Server.sendData(template, ipAddr)
                    while True:
                        Server_data = Server.recvData()
                        if Server_data is not None:
                            data = Server_data[0]
                            print(data)
                            break
                            # if dataInfo.finger_no == data:
                            #     Server.sendData(Access, ipAddr)
                            #     break
                            # elif data == 'break':
                            #     break
                    dataBase.update_count(ipAddr[0], 0)
                    for c in countdata:
                        count = c
                elif count == -2:
                    print(Denied)
                    Server.sendData(Denied, ipAddr)
                    dataBase.update_count(ipAddr[0], 0)
                    for c in countdata:
                        count = c
            else:
                house_no = 'HOUSE' + str(house_no)
                UIDInfo = dataBase.select_sqlData(house_no)
                print(UIDInfo[0])
                UID_no = UIDInfo[1]
                print(UID_no)
                print(data)
                if data == UID_no:
                    countdata = dataBase.select_count(ipAddr[0])
                    for c in countdata:
                        count = c
                    count = count + 1
                    print(count)
                    dataBase.update_count(ipAddr[0], count)
                else:
                    countdata = dataBase.select_count(ipAddr[0])
                    for c in countdata:
                        count = c
                    count = count - 1
                    print(count)
                    dataBase.update_count(ipAddr[0], count)
                if count == 3:
                    print(Access)
                    Server.sendData(Access, ipAddr)
                    dataBase.update_count(ipAddr[0], 0)
                elif count == -3:
                    print(Denied)
                    Server.sendData(Denied, ipAddr)
                    dataBase.update_count(ipAddr[0], 0)


if __name__ == '__main__':
    Main()
