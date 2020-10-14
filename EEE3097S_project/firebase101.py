#connects to database
from firebase import firebase

firebase = firebase.FirebaseApplication('https://welp-2b4f8.firebaseio.com/', None)
new_user = 'Rachel Chitsika','Laurentia Naidu'

#posts user(our) names to the data base
result = firebase.post('/users', new_user, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
print (result)
{u'name': u'TRC'}
{u'name': u'LBN'}
True