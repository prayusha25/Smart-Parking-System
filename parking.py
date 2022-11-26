import random
import sqlite3
import math
import time

conn = sqlite3.connect('parkings.db')
c = conn.cursor()

# c.execute("""CREATE TABLE parkings (Spot int ,
#                                     Vehicle text,
#                                      Time int,
#                                      Coupon int ) """)

conn.commit()


class Parking:
    def __init__(self, spotnum, vehtype, time, couponnum):
        self.spotnum = spotnum
        self.vehtype = vehtype
        self.time = time
        self.couponnum = couponnum

    def generatecoupon():
        return random.randint(1111, 9999)

    def display(self):
        print("\n{} parked at spot {} for {} min.{}".format(self.vehtype, self.spotnum, self.time, self.couponnum))


parklist = []

try:
    print("~WELCOME TO SMART PARKING SYSTEM~")
    time.sleep(2)

    c.execute("SELECT Spot from parkings ")
    spotlist = [x[0] for x in c.fetchall()]
    conn.commit()

    print("\nPark                 : 1")
    print("Unpark               : 2")
    print("Show available spots : 3")
    print("Price information    : 4")

    action = int(input("\nSELECT AN ACTION: "))

    print("\n1 | 2 | 3 | 4 | 5 |")
    print("6 | 7 | 8 | 9 | 10 |\n")

    if action == 1:
        spotnum = int(input("Enter spot number: "))
        if spotnum <= 10 and spotnum > 0:
            temp = spotlist
            spotlist.append(spotnum)
            temp2 = set(spotlist)

            if len(temp) != len(temp2):
                print("\nSpot Occupied! Choose another spot")
            else:
                vehtype = input("Enter vehicle type: ")
                time = int(input("Enter duration in minutes: "))

                if time<0:
                    raise ValueError

                couponnum = Parking.generatecoupon()

                print("\nYour coupon number is: {}".format(couponnum))
                print("Vehicle parked successfully at {} for {} min.".format(spotnum,time))

                park = Parking(spotnum, vehtype, time, couponnum)
                parklist.append(park)

                c.execute("INSERT INTO parkings (Spot, Vehicle, Time, Coupon) VALUES(?,?,?,?)",(park.spotnum, park.vehtype, park.time, park.couponnum))
                conn.commit()
        else:
            print("INVALID SPOT NUMBER!")


    elif action == 2:
        unspot = int(input("ENTER THE SPOT TO UNPARK FROM: "))

        c.execute("SELECT Spot from parkings ")
        scheck = c.fetchone()
        conn.commit()

        if scheck[0] == unspot:
            c.execute("SELECT Coupon from parkings where Spot = ?", (unspot,))
            ccheck = c.fetchone()
            conn.commit()

            uncoupon = int(input("ENTER YOUR COUPON NUMBER: "))

            if uncoupon == ccheck[0]:
                c.execute("SELECT Time from parkings where Spot = ?", (unspot,))
                untime = c.fetchone()
                conn.commit()

                price = untime[0] * 0.8
                print("\nTOTAL PRICE: Rs.{}".format(math.ceil(price)))

                c.execute('DELETE  FROM parkings WHERE Spot = ?', (unspot,))
                conn.commit()
                print("YOU MAY PAY THE PRICE AND UNPARK YOUR VEHICLE!")

            else:
                print("INCORRECT COUPON NUMBER!")

        else:
            print("NOTHING PARKED IN THIS SPOT!")

    elif action == 3:
        spotlist.sort()
        totals = {1,2,3,4,5,6,7,8,9,10}
        sset = set(spotlist)
        availables = totals - sset
        print("AVAILABLE SPOTS: {}".format(availables))

    elif action ==4:
        print("Price will calculated as Rs.0.8/min for any spot.")

    else:
        print("SELECT VALID ACTION!")

except ValueError as ve:
    print("\nInvalid input type! (Enter positive non-zero integer values)")

# c.execute("SELECT * FROM parkings")
# print(c.fetchall())

# c.execute("DELETE from parkings")

# for obj in parklist:
#     obj.display()

conn.commit()
conn.close()








