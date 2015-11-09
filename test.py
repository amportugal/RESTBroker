import json

data= { "title": "New Event",
  "subtitle": "Subtitle of new event",
  "description": "Description of new event",
  "interest": 2,
  "latitude": 8.99309210,
  "longitude": 9.3019203,
  "host": 3,
  "attending": 3,
  "beginning": "2008-04-10 11:47:58",
  "end": "'2008-04-10 11:47:58'",
  "cost": 4,
  "type": "PUB",
  "min_people": 2,
  "max_people": 5 }

reg_ids={"reg_ids" : ["APA91bFtxXJsZXTG8yHBmjW__PbXJ8NXClnr3p7ioUbR9M2IO1irQWhF30MF94-VBW4ixd4JABl6_mj-4XOvfkSYPupXyL25WIje3V7T7L7lHBeHZRmBYvuLGHLu5wOZy3X3Au8Qs7Z_", "2", "3"]}

data_to_send = {key: value for (key, value) in (reg_ids.items() + data.items())}

print data_to_send

