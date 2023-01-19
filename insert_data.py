import pyrebase
from data import config

firebase = pyrebase.initialize_app(config)

db = firebase.database()

# Update data at single location
# db.update({"L1": "1"})

temp_value = db.child('DHT').get('Temperature')
for item in temp_value.each():
    temp_value = item.val()
