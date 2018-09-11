import time
import serial
import datetime
import mysql.connector

prevCount = None

db = {'user': 'checkout', 'password': 'Checkout3022$3022',
      'host': 'studyspace.c08ip18uqlmq.us-east-1.rds.amazonaws.com',
      'database': 'studyspacedb',
      }

while True:
    # set the current count = to  the serial input fom the arduino
    ser = serial.Serial('/dev/ttyACM0',9600)
    x = str(ser.readline())
    curCount = x[2:(len(x)-5)]
    curCount = curCount.strip(' ')
    print(curCount)
    
    # Gathers the current date and time
    currDT = datetime.datetime.now()
    d = currDT.strftime("%Y-%m-%d")
    t = currDT.strftime("%I:%M:%S %p")

    # Tests if the text file has data
    if curCount == " ":
        print('{} {} \t No data'.format(d, t))
        #time.sleep(5)

    # Tests if the current count matches the previous count if not the curr count is pushed to the DB and displayed
    elif curCount != prevCount:
        conn = mysql.connector.connect(**db)

        cursor = conn.cursor()
        #delete = ("DELETE FROM studyspacedb.rooms WHERE RoomID='ISAT3022'")
        
        #cursor.execute(delete)
        data = ('ISAT3022', 'ISAT', 'hello',int(curCount), int(38), 'NO')

        #conn.commit()

       # insert_stmt = (("INSERT INTO rooms (RoomID, BuildingID, Description, CurrentCapacity, TotalCapacity, Reserved) VALUES ('%s', '%s', '%s', %s, %s, '%s')") % \
                    # (data))

        update_stmt = ("UPDATE rooms SET CurrentCapacity=%s WHERE studyspacedb.rooms.RoomID = 'ISAT3022'" % \
		     (curCount))   

        #cursor.execute(insert_stmt)
        cursor.execute(update_stmt)
        conn.commit()
        cursor.close()
        conn.close()
        print("{} {} \t Room count updated to {}".format(d, t, curCount))
        prevCount = curCount
       # time.sleep(5)

    # Prints room count if it is unchanged
    else:
        print('{} {} \t Room count {}'.format(d, t, prevCount))
        #time.sleep(5)
