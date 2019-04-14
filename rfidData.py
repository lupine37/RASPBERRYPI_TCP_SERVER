import sqlite3


conn = sqlite3.connect("rfidData.db")
c = conn.cursor()
rfid2 = ""


class rfidUID:
    def __init__(self, uid_no, name, house_no, card_type, fingerID):
        self.uid_no = uid_no
        self.name = name
        self.house_no = house_no
        self.card_type = card_type
        self.fingerID = fingerID


def GetMaxHouseNo():
    c.execute("SELECT MAX(HOUSE_NO) FROM rfidData")
    for row in c.fetchone():
        return row

    # c.execute("""CREATE TABLE rfidData (
    #           UID_NO TEXT,
    #           NAME TEXT,
    #           HOUSE_NO INTEGER,
    #           CARD_TYPE TEXT
    #           )""")
    # conn.commit()

    # c.execute("""INSERT INTO rfidData VALUES
    #           ('6065654d', 'KENNEDY', 1, 'MASTERCARD'),
    #           ('bbc7c759', 'REGINA', 2, 'ORD')""")
    # conn.commit()


def identification(n):
    list = []
    for L in n:
        list.append(L)
    if list[0] == '$':
        return '$'
    elif list[0] == '#':
        return '#'


def Main(n, d):
    code = identification(n)
    if code == '$':
        rfid = n.replace("$", "")
        rfid2 = rfid
        c.execute("SELECT UID_NO FROM rfidData")
        data = c.fetchall()
        for row in data:
            for column in row:
                if column == rfid:
                    d = d + 1
                    return(d)
                else:
                    d = d - 1
                    return(d)

    elif code == '#':
        print(rfid2)
        c.execute("SELECT FINGERPRINT_ID FROM rfidData")
        data = c.fetchall()
        for row in data:
            for column in row:
                if column == n:
                    return(11)
                else:
                    return(-5)
    return (d)


if __name__ == '__main__':
    Main()
