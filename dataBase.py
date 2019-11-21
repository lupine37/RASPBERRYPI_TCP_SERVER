import sqlite3
import binascii
import struct

conn = sqlite3.connect("LockDatabase.db")
c = conn.cursor()
# imgDir = '/home/pi/Documents/Projects/fingeprintProject/Images/fingerprint1.bmp'

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
    wronglist = (0, 0, 0, 0, 0)
    c.execute("SELECT * FROM MainLock WHERE UID_NO = :uid_no", {'uid_no': n})
    data = c.fetchone()
    if data:
        return(data)
    else:
        return(wronglist)


def select_sqlData(n):
    data = ()
    wronglist = (0, 0)
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


def select_count(n):
    c.execute("SELECT COUNT FROM IPInfo WHERE IP_ADDRESS = :ipAddr",
              {'ipAddr': n})
    count = c.fetchone()
    if count:
        return(count)


def update_count(n, b):
    with conn:
        c.execute("""UPDATE IPInfo SET COUNT = :count
                  WHERE IP_ADDRESS = :ipAddr""",
                  {'count': b, 'ipAddr': n})

def updateTemplate(name, template):
    # print(template)
    with conn:
        c.execute("""UPDATE MainLock SET FINGERPRINT_IMAGE = :image
                   WHERE NAME = :name""", {'name': name, 'image': template})

def selectTemplate(name):
    lst = []
    c.execute("SELECT FINGERPRINT_IMAGE FROM MainLock WHERE NAME = :name", {'name': name})
    data = c.fetchone()
    # print(len(data[0]))
    return(data)
    # print(binascii.hexlify(data[0]))
# updateTemplate('KENNEDY', imgDir)
# selectTemplate('REGINA')
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
