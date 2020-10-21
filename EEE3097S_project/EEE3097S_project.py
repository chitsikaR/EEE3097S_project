"""Main module."""
# First: sudo pigpiod
#load_ext autotime

#import pandas as pd
#import geopandas as gpd
#import json
#import requests
#import geopy
#from geopy.geocoders import Nominatim
#from geopy.extra.rate_limiter import RateLimiter
#import matplotlib.pyplot as plt
#import plotly_express as px
#import tqdm
#from tqdm._tqdm_notebook import tqdm_notebook
from firebase import firebase

from time import sleep
import pigpio
import pynmea2
#import firebase101

pi = pigpio.pi()
addr    = 0x42
bus     = 1
getlen  = 0xFD
getdata = 0xFF
global currentTime
global currentLat
global currentLong
global loc
latitude_test = "0.802"
longitude_test = "0.004"
loc = longitude_test +  "  " + latitude_test
firebase = firebase.FirebaseApplication('https://welp-2b4f8.firebaseio.com/', None)
#new_user = 'Rachel Chitsika','Laurentia Naidu'
#result = firebase.post('/users', new_user, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
#print (result)
#{u'name': u'TRC'}
#{u'name': u'LBN'}
True

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


# post GPS data to database - Rachel
def postGPSDatatoDB():
    gps = firebase.post('/Latitude',latitude_test)
    gps2 = firebase.post ('/Longitute', longitude_test) 
    gpsLocation = firebase.post('/Location', loc)
    print (gpsLocation)
    pass

# Rachel
# gets the current location of the user as (lat, long)
def getCurrentLocation():
    location_ = firebase.get('/Location', '').limitToLast
    return (location_)
    pass

# Laurentia
# get last 20 locations from DB. possibly with address
def getMostRecentLocations():
    pass

# Laurentia
# generate message as string
def getTextMessage():
    global currentLat
    global currentLong
    global currentTime
    currentLat = float(0.2)
    currentLong = float(0.24)
    currentTime = "23:15"
    text_message = "***DISTRESS SIGNAL*** \n"
    #text_message = text_message+"Time: "+currentTime+"\n"
    text_message = text_message+"Laurentia is in danger now at:\n"
    text_message = text_message+getAddress()+"\n"
    text_message = text_message+("Lat: "+ "{:.2f}".format(currentLat)+" Long: "+"{:.2f}".format(currentLong))
    return text_message
    

# Laurentia
# use lat and long to get address
#def getAddress():
 #   locator = Nominatim(user_agent="myGeocoder")
  #  currentCoordinates = getCurrentLocation
    #coordinates = "-26.140671, 27.856640"
   # location = locator.reverse(currentCoordinates)
   # location.raw
   # return (location.address)

    

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
        sleep(120) # read data every 2 minutes


if __name__ == "__main__":
    postGPSDatatoDB()
