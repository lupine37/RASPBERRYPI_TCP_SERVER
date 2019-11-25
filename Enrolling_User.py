import struct
import time
from pyfingerprint2 import PyFingerprint
import binascii
import dataBase
import MFRC522
import RPi.GPIO as GPIO

pack = [0xef01, 0xffffffff, 0x2]
Reader = MFRC522.MFRC522()
GPIO.setwarnings(False)



def readRFID():
    while True:
        status, TagType = Reader.MFRC522_Request(Reader.PICC_REQIDL)
        if status == Reader.MI_OK:
            print ("Card detected")

        status, uid = Reader.MFRC522_Anticoll()
        if status == Reader.MI_OK:
            a = str(hex(uid[0])[2:])
            b = str(hex(uid[1])[2:])
            c = str(hex(uid[2])[2:])
            d = str(hex(uid[3])[2:])
            uid_s = a + b + c + d
            key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

            Reader.MFRC522_SelectTag(uid)

            status = Reader.MFRC522_Auth(Reader.PICC_AUTHENT1A, 8, key, uid)

            if status == Reader.MI_OK:
                Reader.MFRC522_Read(8)
                Reader.MFRC522_StopCrypto1()
                break
            else:
                print("Authentication error")
                break
    GPIO.cleanup()
    return uid_s


def downloadTemplate():
    l = 0
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        
        if (f.verifyPassword() == False):
            raise ValueError('The given fingerprint Sensor password is wrong')

    except Exception as e:
        print('The fingerprint sensor could not be initialized')
        print('Exception message: ' + str(e))
        exit(1)

    try:
        print('Waiting for finger...')
        time.sleep(2)
        while (f.readImage() == False):
            pass
            
        f.convertImage(0x01)

        print('Remove finger finger...')
        time.sleep(2)

        print('Waiting for same finger again...')
        time.sleep(2)
        while (f.readImage() == False):
            pass

        f.convertImage(0x02)
        # uploadTemplate('KENNEDY')

        if (f.compareCharacteristics() == 0):
            return('Finger do not match')
        
        else:
            print("fingerprint match")
            print(f.compareCharacteristics())
        
        f.createTemplate()
        characteristicData = f.downloadCharacteristics()
        l = len(characteristicData)
        form = 'B' * l
        temp = struct.pack(form, *characteristicData)
        return temp
        
        
    except Exception as e:
        print('Operation failed!')
        print('Exeption message: ' + str(e))
        exit(1)

def uploadTemplate(name):
    lst = []
    lst1 = []
    dBret = []
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        
        if (f.verifyPassword() == False):
            raise ValueError('The given fingerprint Sensor password is wrong')

    except Exception as e:
        print('The fingerprint sensor could not be initialized')
        print('Exception message: ' + str(e))
    dBret = dataBase.selectTemplate(name)
    
    l = len(dBret[0])
    # print(dBret[0])
    # print(binascii.hexlify(dBret[0]))
    form = 'B' * l
    lst1.extend(struct.unpack(form, dBret[0]))
    # # print(lst1)
    character = f.uploadCharacteristics(0x02, lst1)
    # # print(list)
    print(character)

def Main():
    while True:
        response  = input("TO ADD OR REMOVE A CARD OR EXIT: ")
        if response == 'ADD':
            print("PLACE YOUR CARD")
            cardUID = readRFID()
            print(cardUID)
            cardState = dataBase.select_uidNo(cardUID)
            if cardState == 1:
                print("already Exist")
            elif cardState == 0:
                name = input("NAME: ")
                house_no = input("HOUSE NO: ")
                cardType = input("CARD TYPE: ")
                fingerTemp = downloadTemplate()
                dataBase.addUser(house_no, name, cardUID, cardType, fingerTemp)
        elif response == 'REMOVE':
            print("PLACE YOUR CARD")
            cardUID = readRFID()
            cardState = dataBase.select_uidNo(cardUID)
            if cardState == 0:
                print("Card does not exist")
            elif cardState == 1:
                name = dataBase.getName(cardUID)
                response2 = input("ARE YOU SURE FOR REMOVING " + name + ": ")
                if response2 == 'YES':
                    dataBase.removeUser(cardUID)
                else:
                    pass
        elif response == 'EXIT':
            print("Exit from Enrolling")
            break
                

if __name__ == "__main__":
    Main()