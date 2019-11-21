import struct
from pyfingerprint2 import PyFingerprint
import time
import binascii
import dataBase

pack = [0xef01, 0xffffffff, 0x2]

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


def AddInstructionTemplates(data):
    lst = []
    str_f = 'B'  * len(data)  
    lst.extend(struct.unpack(str_f, data))
    pack2 = pack + [(len(lst) + 2)]
    a = sum(pack2[-2:]) + sum(data)
    s = struct.pack('@I', a)
    print(s)
    # pack_str = '@HIBH' + 'B' * len(data) + 'H'
    # l = pack2 + data + a
    # s = struct.pack(pack_str, *l)
    # print(s)

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
        # time.sleep(2)

        # print('Waiting for same finger again...')
        # time.sleep(2)
        # while (f.readImage() == False):
        #     pass

        # f.convertImage(0x02)
        uploadTemplate('KENNEDY')

        if (f.compareCharacteristics() == 0):
            raise Exception('Finger do not match')
        
        else:
            print("fingerprint match")
            # print(f.compareCharacteristics())
        
        # f.createTemplate()
        # characteristicData = f.downloadCharacteristics()
        # print(characteristicData)
        # l = len(characteristicData)
        # print(l)
        # form = 'B' * l
        # temp = struct.pack(form, *characteristicData)
        # print(temp)
        # dataBase.updateTemplate('REGINA', temp)
        
        
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
    

downloadTemplate()
# uploadTemplate('REGINA')