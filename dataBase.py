import sqlite3
import binascii
import struct

conn = sqlite3.connect("LockDatabase.db")
c = conn.cursor()
# imgDir = '/home/pi/Documents/Projects/fingeprintProject/Images/fingerprint1.bmp'

def select_sqlData(n):
    data = ()
    wronglist = (0, 0, 0, 0, 0)
    c.execute("SELECT * FROM rfidData WHERE UID_NO = :uid_no", {'uid_no': n})
    data = c.fetchone()
    if data:
        return(data)
    else:
        return(wronglist)

def update_port_count(b):
    print(b[1])
    with conn:
        c.execute("""UPDATE IPInfo SET PORT = :port, COUNT  = :count
                  WHERE IP_ADDRESS = :ip""",
                  {'ip': b[0], 'port': b[1], 'count': 0})


def select_IPAddr(n):
    c.execute("SELECT IP_ADDRESS, PORT FROM IPInfo WHERE HOUSE_NO = :house_no",
              {'house_no': n})
    ipAddr = c.fetchone()
    return(ipAddr)


def select_sqlMainData(n):
    data = ()
    wronglist = (0, 0, 0, 0, 0, 0)
    c.execute("SELECT * FROM MainLock WHERE UID_NO = :uid_no", {'uid_no': n})
    data = c.fetchone()
    if data:
        return(data)
    else:
        return(wronglist)


def select_sqlData(n):
    data = ()
    query = "SELECT * FROM " + n
    c.execute(query)
    data = c.fetchone()
    if data:
        return(data)


def select_house_no(n):
    c.execute("SELECT HOUSE_NO FROM IPInfo WHERE IP_ADDRESS = :ipAddr",
              {'ipAddr': n})
    house_no = c.fetchone()
    if house_no:
        return(house_no)

def select_uidNo(uid_no):
    c.execute("SELECT EXISTS(SELECT 1 FROM MainLock WHERE UID_NO = :uid)",
              {'uid': uid_no})
    data, = c.fetchone()
    return(data)

def addUser(house_no, name, uid_no, cardType, fingerTemplate):
    with conn:
        c.execute("""INSERT INTO MainLock 
                  VALUES(:house, :name, :uid, :card, :temp, :state)""",
                  {'house': house_no, 'name': name, 'uid': uid_no, 'card': cardType,
                   'temp': fingerTemplate, 'state': 0})


def updateTemplate(uid_no, template):
    # print(template)
    with conn:
        c.execute("""UPDATE MainLock SET FINGERPRINT_TEMPLATE = :image
                   WHERE UID_NO = :uid""", {'uid': uid_no, 'image': template})

def selectTemplate(uid_no):
    c.execute("SELECT FINGERPRINT_TEMPLATE FROM MainLock WHERE UID_NO = :uid", {'uid': uid_no})
    data = c.fetchone()
    return(data)

def checkEntryState(uid_no):
    c.execute("SELECT ENTRY_STATE FROM MainLock WHERE UID_NO = :uid", {'uid': uid_no})
    data = c.fetchone()
    return data

def updateEntryState(uid_no, entryState):
    with conn:
        c.execute("UPDATE MainLock SET ENTRY_STATE = :entry WHERE UID_NO = :uid",
         {'entry': entryState, 'uid': uid_no})

def getName(uid_no):
    c.execute("SELECT NAME FROM MainLock WHERE UID_NO = :uid", {'uid': uid_no})
    data, = c.fetchone()
    return data

def removeUser(uid_no):
    with conn:
        c.execute("DELETE FROM MainLock WHERE UID_NO = :uid", {'uid': uid_no})
    # def add_sqlData(n):
    #     list = []
    #     idNo = 0
    #     n = n.replace(" ", "")
    #     for line in n:
    #         list.append(line)
    #     n = ''.join(list[0:8])
    #     uid_no = ""
    #     c.execute("SELECT UID_NO FROM rfidData WHERE CARD_TYPE = 'MASTERCARD'")
    #     cardInfo = c.fetchone()
    #     c.execute("SELECT UID_NO FROM rfidData WHERE UID_NO = :uid_no",
    #               {'uid_no': n})
    #     data = c.fetchone()
    #     try:
    #         for raw in cardInfo:
    #             MasterCard = raw
    #         for raw in data:
    #             uid_no = raw
    #     except Exception:
    #         pass
    #     finally:
    #         if n == MasterCard:
    #             print("Try Again")
    #         else:
    #             if uid_no == n:
    #                 print("ALREADY EXIST")
    #             else:
    #                 name = input("NAME: ")
    #                 house_no = input("HOUSE NO: ")
    #                 idNo = EnrollFingerID(house_no)
    #                 if idNo != 0:
    #                     print(idNo)
    #                     with conn:
    #                         c.execute("""INSERT INTO rfidData VALUES
    #                                   (:house_no, :name, :uid_no, :card_type,
    #                                    :idNo)""",
    #                                   {'house_no': house_no, 'name': name,
    #                                    'uid_no': n, 'card_type': 'ORD',
    #                                    'idNo': idNo})
    #                     print("ADDED")
    #
    #
    # def Remove_sqlData(n):
    #     list = []
    #     n = n.replace(" ", "")
    #     for line in n:
    #         list.append(line)
    #     n = ''.join(list[0:8])
    #     uid_no = ""
    #     c.execute("SELECT UID_NO FROM rfidData WHERE CARD_TYPE = 'MASTERCARD'")
    #     cardInfo = c.fetchone()
    #     c.execute("SELECT UID_NO FROM rfidData WHERE UID_NO = :uid_no",
    #               {'uid_no': n})
    # try:
    #         for raw in cardInfo:
    #             MasterCard = raw
    #         for raw in data:
    #             uid_no = raw
    #     except TypeError:
    #         print("card Does Not Exist")
    #     finally:
    #         if n == MasterCard:
    #             print("Try Again")
    #         else:
    #             if uid_no == n:
    #                 with conn:
    #                     c.execute("""DELETE FROM rfidData WHERE UID_NO =
    #                                   :uid_no""",
    #                               {'uid_no': n})
