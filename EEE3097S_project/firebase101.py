#connects to database
from firebase import firebase

firebase = firebase.FirebaseApplication('https://welp-2b4f8.firebaseio.com/', None)
new_user = 'Rachel Chitsika','Laurentia Naidu'
latitude = "00145"
longitude = "001889"
loc = longitude +  "  " + latitude

#def postGPSDatatoDB():
gps = firebase.post('Latitude',latitude)
gps2 = firebase.post ('Longitute', longitude) 
gpsLocation = firebase.post('Location', loc)
print (gps)
print (gps2)
print (gpsLocation)
    
#get location from database
location_ = firebase.get('/Location', '')
print(location_)
#posts user(our) names to the data base
result = firebase.post('/users', new_user, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
print (result)
{u'name': u'TRC'}
{u'name': u'LBN'}
True