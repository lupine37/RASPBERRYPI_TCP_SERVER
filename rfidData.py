import sqlite3


conn = sqlite3.connect("rfidData.db")
c = conn.cursor()


class rfidUID:
    def __init__(self, uid_no, name, house_no, card_type):
        self.uid_no = uid_no
        self.name = name
        self.house_no = house_no
        self.card_type = card_type


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


def Main(n, d):
    c.execute("SELECT UID_NO FROM rfidData")
    data = c.fetchall()
    for row in data:
        for column in row:
            if column == n:
                d = d + 1
                return(d)
            else:
                d = d - 1
                return(d)


if __name__ == '__main__':
    Main()
