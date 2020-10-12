"""Main module."""
# First: sudo pigpiod

from time import sleep
import pigpio
import pynmea2

pi = pigpio.pi()
addr    = 0x42
bus     = 1
getlen  = 0xFD
getdata = 0xFF
global currentTime
global currentLat
global currentLong

# get location data from GPS module
# adapted from https://github.com/xinabox/Python-SN01.git
def getSN01_data():
    rl =0
    handle = pi.i2c_open(bus, addr)
    try:
        dl = pi.i2c_read_word_data(handle, getlen)//256
        if dl>0:
            (rl,data) = pi.i2c_zip(handle,[4,addr, 7,1,getdata, 6,dl, 0])
    except:
        pass
    pi.i2c_close(handle) 
    if rl>0:
        return data.decode(encoding='UTF-8',errors='ignore').splitlines()
    return None


# post GPS data to database
def postGPSDatatoDB():
    pass

# get last 20 locations from DB. possibly with address
def getMostRecentLocations():
    pass

# generate message as string
def getTextMessage():
    pass

# use lat and long to get address
def getAddress():
    pass


# i edited this to save the data to variables
def formatData():
    global currentTime
    global currentLat
    global currentLong

    while(True):
        data = getSN01_data()
        if data:
            for t in data:
                try:
                    msg = pynmea2.parse(t,check=True)
                    currentTime = msg.timestamp
                    currentLat = msg.latitude
                    currentLong = msg.longitude
                    print(msg.timestamp, msg.latitude, msg.longitude)
                except:
                    pass
        sleep(160) # read data every 2 minutes