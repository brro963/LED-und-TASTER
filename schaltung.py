import RPi.GPIO as GPIO
import time
import sqlite3
import datetime
GPIO.setwarnings(False)
class Diode:
        def __init__(self,pin):
                self.diode_number = pin
                self.status = False
                GPIO.setup(pin,GPIO.OUT)
        def DIODEON(self):
                GPIO.output(self.diode_number, GPIO.HIGH)
                self.status = True
        def DIODEOFF(self):
                GPIO.output(self.diode_number, GPIO.LOW)
                self.status = False

class Button:
    def __init__(self,pin):
        self.Button_number = pin
        self.status = False
        GPIO.setup(pin, GPIO.IN)

    def BUTTON_abchecken(self):
        if GPIO.input(self.Button_number):
           self.status = True
           return True
        else:
            return False
            self.status = False

class Database:
        def __init__(self):
                self.connection = sqlite3.connect('zeit.db')
                self.connect = self.connection.cursor()
        def Create_db(self):
                self.connect.execute('''CREATE TABLE Zeit
                             (zeitstempel, diode_zustand )''')
                self.connection.commit()
        def write(self, zeit, diode_zustand):
                self.connect.execute("INSERT INTO Zeit VALUES ('" + zeit + "','" + diode_zustand + "')")
                self.connection.commit()
class PROGRAM:
        def __init__(self):
                GPIO.setmode(GPIO.BOARD)
                self.button = Button(13)
                self.diode = Diode(11)
                self.Database = Database()
        def controlling(self):
                if self.button.BUTTON_abchecken():
                        x = datetime.datetime.now()
                        print(x)
                        while self.button.status == True:
                                time.sleep(0.3)
                                if self.button.BUTTON_abchecken() == False:
                                        break
                        y = datetime.datetime.now()
                        zeit = y-x
                        print(zeit)
                        if zeit.seconds > 0: 
                                pass

                        else:
                                if self.diode.status == False:
                                        self.diode.DIODEON()
                                        self.Database.write(time.asctime(time.localtime(time.time())), "diode an")
                                else:
                                        self.diode.DIODEOFF()
                                        self.Database.write(time.asctime(time.localtime(time.time())), "diode aus")
try:
        Database().Create_db()
except sqlite3.OperationalError:
        pass     
Start = PROGRAM()
try:
        while True:
                Start.controlling()
except: KeyboardInterrupt
time.sleep(0.5)
GPIO.cleanup()


