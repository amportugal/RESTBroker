from flask import Flask, request
import requests
import httplib
import json

app = Flask(__name__)

@app.route('/user/', methods=['POST'])
def registerUser():
    #Obtain JSON from message
    json_msg=request.data

    #Decode it
    json_decoded=json.loads(json_msg)

    #build new json message
    interests=json_decoded['interests']
    username=json_decoded['username']
    longitude=json_decoded['longitude']
    latitude=json_decoded['latitude']
    password=json_decoded['hashedPW']
    timestamp=json_decoded['timestamp']


    new_json={"username": username, "hashedPW": password}
    #Authentication service
    #TODO: insert url
    #auth_rest_url=''
    #response=requests.POST(auth_rest_url, new_json)

    #json_decoded=json.loads(response.text)

    #if response.status_code!=httplib.CREATED:
    #    response_json = {"code": httplib.FORBIDDEN, "reason": json_decoded['reason']}
    #    return response_json

    new_json={ "id" : username, "longitude" : longitude, "latitude" : latitude, "interests" : interests, "timestamp": timestamp}
    #Location service
    loc_rest_url='http://192.168.8.217:4180/api/user'
    response=requests.POST=(loc_rest_url, new_json)

    json_decoded=json.loads(response.text)

    if response.status_code!=httplib.CREATED:
        #Delete the previously created username
        #TODO: insert url
        auth_rest_url=''
        response=requests.DELETE(auth_rest_url, {"username" : username})
        response_json = {"code": httplib.FORBIDDEN, "reason": json_decoded['reason']}
        return response_json

    response_json={"code": httplib.CREATED, "reason": "none"}

    return response_json

#EditUser
@app.route('/user/', methods=['PUT'])
def editUser():
    #Obtain JSON from message
    json_msg=request.data

    #Location service
    #TODO: insert url
    loc_rest_url=''
    data = json_msg
    response = requests.PUT(loc_rest_url, data)

    if response.status_code!=httplib.OK:
        response_json = {"code": httplib.FORBIDDEN, "reason": response.text}
        return response_json

    response_json = {"code": httplib.OK, "reason": 'none'}

    return response_json

#Login
@app.route('/login/', methods=['GET'])
def login():
    #Obtain JSON from message
    json_msg=request.data

    #Auth service
    #TODO: insert url
    auth_rest_url=''
    data = json_msg
    response = requests.GET(auth_rest_url, data)

    if response.status_code!=httplib.OK:
        response_json = {"code": httplib.FORBIDDEN, "reason": response.text}
        return response_json

    response_json={"code": httplib.OK, "reason": "none"}

    return response_json


#Create Event
@app.route('/event/', methods=['POST'])
def createEvent():
    #Obtain json message
    json_msg=request.data


    #Location service: send event creation
    #rest_url='http://192.168.8.217:4180/api/event/'
    #response = requests.post(rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"}, data=json_msg)

    #print response.text
    #if response.status_code!=httplib.OK:
    #    return response

    json_decoded=json.loads(json_msg)
    #json_get_users={"latitude": json_decoded['latitude'], "longitude": json_decoded['longitude'], "interest": json_decoded['interest']}
    #rest_url='http://192.168.8.217:4180/api/user/nearest&limit=' + str(json_decoded['min_people'])
    #response = requests.post(rest_url, data=json_get_users)

    #TODO: Extract reg_ids from the json_msg to variable data_to_send
    #json_users=json.loads(response.text)

    #for user in json_users['results']:

    #TODO: TILL HERE

    #static data
    reg_ids={"reg_ids" : ["APA91bFtxXJsZXTG8yHBmjW__PbXJ8NXClnr3p7ioUbR9M2IO1irQWhF30MF94-VBW4ixd4JABl6_mj-4XOvfkSYPupXyL25WIje3V7T7L7lHBeHZRmBYvuLGHLu5wOZy3X3Au8Qs7Z_"]}

    data_to_send = {key: value for (key, value) in (reg_ids.items() + json_decoded.items())}

    #Notification
    #TODO: Localhost to be changed
    rest_url='http://localhost:8888/sendEventCreateNotification'
    r = requests.get(url=rest_url, data=json.dumps(data_to_send))

    response_json={"code": httplib.CREATED, "reason": "none"}


    return response_json

#Edit Event
@app.route('/event/', methods=['PUT'])
def editEvent():
    #Obtain json message
    json_msg=request.data()

    print json_msg

    #Location service: send event creation
    rest_url='http://192.168.8.217:4180/api/event/' + "30" + "/"#TODO: json_msg["event_id"]
    response = requests.put(rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"}, data=json_msg)

    print response.status_code

    if response.status_code!=httplib.OK:
        return response


    json_decoded=json.loads(json_msg)
    rest_url='http://192.168.8.217:4180/api/user/attending/event/' + "30" + "/" #TODO: json_msg["event_id"]
    response = requests.get(rest_url, "")

    print response.text

    #TODO: Extract reg_ids from the json_msg to variable data_to_send
    #json_users=json.loads(response.text)

    #for user in json_users['results']:

    #TODO: TILL HERE

    #static data
    reg_ids={}#={"reg_ids" : ["APA91bFtxXJsZXTG8yHBmjW__PbXJ8NXClnr3p7ioUbR9M2IO1irQWhF30MF94-VBW4ixd4JABl6_mj-4XOvfkSYPupXyL25WIje3V7T7L7lHBeHZRmBYvuLGHLu5wOZy3X3Au8Qs7Z_"]}

    data_to_send = {key: value for (key, value) in (reg_ids.items() + json_decoded.items())}

    #Notification
    #TODO: Localhost to be changed
    rest_url='http://localhost:8888/sendEventUpdateNotification'
    r = requests.get(url=rest_url, data=json.dumps(data_to_send))

    response_json={"code": httplib.OK, "reason": "none"}

    return response_json

#Delete Event
@app.route('/event/', methods=['DELETE'])
def deleteEvent():
    #Obtain json message
    json_msg=request.data()

    #Location service: send event creation
    #rest_url='http://192.168.8.217:4180/api/event/' + "30" + "/" #TODO: json_msg["event_id"]
    #response = requests.delete(rest_url,  headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"}, data="")


    #if response.status_code!=httplib.CREATED:
    #    return response


    json_decoded=json.loads(json_msg)
    #rest_url='http://192.168.8.217:4180/api/user/attending/event/' + "3" #TODO: json_msg["event_id"]
    #response = requests.get(rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"}, data="")

    #static data
    reg_ids={"reg_ids" : ["APA91bFtxXJsZXTG8yHBmjW__PbXJ8NXClnr3p7ioUbR9M2IO1irQWhF30MF94-VBW4ixd4JABl6_mj-4XOvfkSYPupXyL25WIje3V7T7L7lHBeHZRmBYvuLGHLu5wOZy3X3Au8Qs7Z_"]}

    data_to_send = {key: value for (key, value) in (reg_ids.items() + json_decoded.items())}

    #Notification
    rest_url='http://localhost:8888/sendEventDeletionNotification'
    r = requests.get(url=rest_url, data=json.dumps(data_to_send))

    response_json={"code": httplib.CREATED, "reason": "none"}

    return response_json

#Search Event
@app.route('/event/', methods=['GET'])
def searchEvent():
    pass

#Join User to Event
@app.route('/joinUserToEvent/', methods=['POST'])
def joinUserToEvent():
    # json_msg=web.data()
    # json_decoded = json.loads(json_msg)

    # get user id from joao
    # user_id = json_decoded['user_id']
    user_id = 1

    # get event id from johny boy
    # event_id = json_decoded['event_id']
    event_id = 1

    # do the joiningz man
    rest_url='http://192.168.8.217:4180/api/event/attending/' + user_id + '/'
    response = requests.PUT(rest_url, {'event_id': event_id})

    response_json={"code": httplib.OK, "reason": "none"}
    return response_json

#Delete User to Event
@app.route('/deleteUserToEvent/', methods=['DELETE'])
def deleteUserToEvent():
    # json_msg=web.data()
    # json_decoded = json.loads(json_msg)

    # get user id from joao
    # user_id = json_decoded['user_id']
    user_id = 1

    # get event id from johny boy
    # event_id = json_decoded['event_id']
    event_id = 1

    # do the deletingz man
    rest_url='http://192.168.8.217:4180/api/event/attending/' + user_id + '/'
    response = requests.DELETE(rest_url, {'event_id': event_id})

    response_json={"code": httplib.OK, "reason": "none"}
    return response_json

#Get Users Near Event
@app.route('/getUsersNearEvent/', methods=['GET'])
def getUsersNearEvent():
    # json_msg=web.data()
    # json_decoded = json.loads(json_msg)

    # get event id from johny boy
    # event_id = json_decoded['event_id']
    event_id = 1

    # get event from ivo san
    rest_url='http://192.168.8.217:4180/api/event/' + event_id + '/'
    response = requests.GET(rest_url)

    # get nearest users from ivo san
    event = json.loads(response.text)
    longitude = event['longitude']
    latitude = event['latitude']
    interest = event['interest']

    # do the deletingz man
    rest_url='http://localhost:8000/api/user/nearest/'
    response = requests.GET(rest_url, {'longitude': longitude,
                                          'latitude': latitude,
                                          'interest': interest})

    response_json={"code": httplib.OK, "reason": "none"}
    return response_json



if __name__ == '__main__':
    app.run(port=8888)
