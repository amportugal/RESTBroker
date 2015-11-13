from flask import Flask, request
from flasgger import Swagger
import requests
import httplib
import json

app = Flask(__name__)

Swagger(app)

@app.route('/user/', methods=['POST'])
def registerUser():
    """
    Register user
    Registers an user.
    Expects the following JSON:


    ---
    tags:
      - User
    responses:
      200:
        description: A single user item
        schema:
          id: return_test
          properties:
            result:
              type: string
              description: The test
              default: 'test'
    """
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
def editUserInfo():
    """
    Edit user
    Edits information of a user.
    Expects user_id.
    Expects the following JSON:
    {
        "latitude": 9.123
        "longitude": 8.123
        "interests": ["futebol", "tetris"]
    }

    ---
    tags:
      - User
    responses:
      200:
        description: A single user item
        schema:
          id: return_json
          properties:
            code:
              type: integer
              description: The HTTP response code
              default: '200'
            reason:
              type: string
              description: The reason of not updating a user
              default: ''
    """
    #Obtain JSON from message
    json_msg=request.data

    #Location service
    loc_rest_url='http://192.168.8.217:4180/api/user/' + json_msg['user_id'] + '/'
    data = json_msg
    response = requests.PUT(loc_rest_url, data)

    if response.status_code!=httplib.OK:
        response_json = {"code": httplib.FORBIDDEN, "reason": "Could not update user."}
        return response_json

    response_json = {"code": httplib.OK, "reason": 'none'}

    return response_json

@app.route('/user/', methods=['DELETE'])
def removeUser():
    """
    Delete user
    Deletes a user.
    Expects: user_id.

    ---
    tags:
      - User
    responses:
      200:
        description: A single user item
        schema:
          id: return_test
          properties:
            result:
              type: string
              description: The test
              default: 'test'
    """
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
    """
    User log in
    User logs in.
    Expects the following JSON:

    ---
    tags:
      - User
    responses:
      200:
        description: A single user item
        schema:
          id: return_test
          properties:
            result:
              type: string
              description: The test
              default: 'test'
    """
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
    """
    Create event
    Creates an event.
    Expects the following JSON:
    {
        "longitude": 1.234,
        "latitude": 2.343,
        "title": "title",
        "subtitle": "subtitle", (opcional)
        "description": "event description",
        "beginning": "15-03-2004T00:24:00",
        "end": "15-03-2004T00:24:00", (opcional)
        "cost": 2, (opcional)
        "host": 2,
        "type": False,
        "min_people": 40,
        "max_people": 100, (opcional)
        "interest": "Swag",
        "image" : "image/event_01.jpg" (opcional)
    }

    ---
    tags:
      - Event
    responses:
      201:
        description: A single user item
        schema:
          id: return_json
          properties:
            code:
              type: integer
              description: The HTTP response code
              default: '201'
            reason:
              type: string
              description: The reason of a not-created event
              default: ''
            event_id:
              type: int
              description: Event identification
              default: '2'
    """
    #Obtain json message
    json_msg=request.data

    #Location service: send event creation
    rest_url='http://192.168.8.217:4180/api/event/'
    response = requests.post(rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"}, data=json_msg)

    #print response.text
    if response.status_code!=httplib.OK:
        return response

    json_decoded=json.loads(json_msg)
    json_get_users={"latitude": json_decoded['latitude'], "longitude": json_decoded['longitude'], "interest": json_decoded['interest']}
    rest_url='http://192.168.8.217:4180/api/user/nearest&limit=' + str(json_decoded['min_people'])
    response = requests.post(rest_url, data=json_get_users)

    event_id=response.text

    #TODO: Extract reg_ids from the json_msg to variable data_to_send
    #json_users=json.loads(response.text)

    #for user in json_users['results']:

    #TODO: TILL HERE

    #static data
    reg_ids={"reg_ids" : ["APA91bFtxXJsZXTG8yHBmjW__PbXJ8NXClnr3p7ioUbR9M2IO1irQWhF30MF94-VBW4ixd4JABl6_mj-4XOvfkSYPupXyL25WIje3V7T7L7lHBeHZRmBYvuLGHLu5wOZy3X3Au8Qs7Z_"]}

    data_to_send = {key: value for (key, value) in (reg_ids.items() + json_decoded.items())}

    #Notification
    rest_url='http://localhost:8080/sendEventCreateNotification'
    r = requests.get(url=rest_url, data=json.dumps(data_to_send))

    response_json={"code": httplib.CREATED, "reason": "none", "event_id": event_id}


    return response_json

#Edit Event
@app.route('/event/', methods=['PUT'])
def editEvent():
    """
    Edit event
    Edits an event.
    Expects the event id as parameter.
    Expects the following JSON:
    {
        "longitude": 1.234, (opcional)
        "latitude": 2.343, (opcional)
        "title": "title", (opcional)
        "subtitle": "subtitle", (opcional)
        "description": "event description", (opcional)
        "beginning": "15-03-2004T00:24:00", (opcional)
        "end": "15-03-2004T00:24:00", (opcional)
        "cost": 2, (opcional)
        "type": False, (opcional)
        "min_people": 40, (opcional)
        "max_people": 100, (opcional)
        "interest": "Swag" (opcional)
    }
    ---
    tags:
      - Event
    responses:
      200:
        description: A single user item
        schema:
          id: return_json
          properties:
            code:
              type: integer
              description: The HTTP response code
              default: '200'
            reason:
              type: string
              description: The reason of a not-created event
              default: ''
    """
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
    rest_url='http://localhost:8080/sendEventUpdateNotification'
    r = requests.get(url=rest_url, data=json.dumps(data_to_send))

    response_json={"code": httplib.OK, "reason": "none"}

    return response_json

#Delete Event
@app.route('/event/', methods=['DELETE'])
def deleteEvent():
    """
    Delete event
    Delete an event.
    Expects the event_id as parameter.

    ---
    tags:
      - Event
    responses:
      200:
        description: A single user item
        schema:
          id: return_json
          properties:
            code:
              type: integer
              description: The HTTP response code
              default: '200'
            reason:
              type: string
              description: The reason of a not-created event
              default: ''
    """
    #Obtain json message
    event_id=request.data()

    #Location service: send event creation
    rest_url='http://192.168.8.217:4180/api/event/' + event_id + "/"
    response = requests.delete(rest_url,  headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"})


    if response.status_code!=httplib.CREATED:
        return response


    rest_url='http://192.168.8.217:4180/api/user/attending/event/' + event_id + "/"
    response = requests.get(rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"})

    # TODO: static data
    reg_ids={"reg_ids" : ["APA91bFtxXJsZXTG8yHBmjW__PbXJ8NXClnr3p7ioUbR9M2IO1irQWhF30MF94-VBW4ixd4JABl6_mj-4XOvfkSYPupXyL25WIje3V7T7L7lHBeHZRmBYvuLGHLu5wOZy3X3Au8Qs7Z_"]}

    data_to_send = {key: value for (key, value) in (reg_ids.items() + json_decoded.items())}

    #Notification
    rest_url='http://localhost:8080/sendEventDeletionNotification'
    r = requests.get(url=rest_url, data=json.dumps(data_to_send))

    response_json={"code": httplib.CREATED, "reason": "none"}

    return response_json

#Search Event
@app.route('/event/', methods=['GET'])
def searchEvent():
    """
    Search for event
    Searches for an event.
    Expects the id as parameter.

    ---
    tags:
      - Event
    responses:
      200:
        description: A single user item
        schema:
          id: return_json
          properties:
            code:
              type: integer
              description: The HTTP response code
              default: '200'
            info:
              type: string
              description: The reason of a not-created event
              default: '{
                    "longitude": 1.234,
                    "latitude": 2.343,
                    "title": "title",
                    "subtitle": "subtitle",
                    "description": "event description",
                    "beginning": "15-03-2004T00:24:00",
                    "end": "15-03-2004T00:24:00", (opcional)
                    "cost": 2,
                    "type": False,
                    "min_people": 40,
                    "max_people": 100,
                    "interest": "Swag"
                }'
    """
    #Obtain event_id
    event_id=request.data()

    #Location service: send event creation
    rest_url='http://192.168.8.217:4180/api/event/' + event_id + '/'
    response = requests.get(rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"})

    if response.status_code!=httplib.OK:
        return response

    response_json={"code": httplib.OK, "reason": "none", "info": response.text}

    return response_json


#Get Nearest Events
@app.route('/getNearestEvents/', methods=['GET'])
def getNearestEvents():
    """
    Get Nearest events
    Obtains all the events near the user.
    Expects the user_id as parameter.

    ---
    tags:
      - Event
    responses:
      200:
        description: A single user item
        schema:
          id: return_json
          properties:
            code:
              type: integer
              description: The HTTP response code
              default: '200'
            info:
              type: string
              description: All the events info.
              default: 'e.g. http://pastebin.com/tk0TncXu'
    """

    #Obtain event_id
    user_id=request.data()

    #Location service: send event creation
    rest_url='http://192.168.8.217:4180/api/event/nearest' + user_id + '/'
    response = requests.get(rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"})

    if response.status_code!=httplib.OK:
        return response

    response_json={"code": httplib.OK, "reason": "none", "info": response.text}

    return response_json

#Join User to Event
@app.route('/joinUserToEvent/', methods=['POST'])
def joinUserToEvent():
    """
    Join user to event
    Joins a user to a certain event.
    Expects user_id, event_id.

    ---
    tags:
      - User on Event
    responses:
      200:
        description: A single user item
        schema:
          id: return_json
          properties:
            code:
              type: integer
              description: The HTTP response code
              default: '200'
            reason:
              type: string
              description: The reason of user not joining an event
              default: ''
    """

    json_decoded = json.loads(request.data)

    # get user id from joao
    user_id = json_decoded['user_id']
    #user_id = 1

    # get event id from johny boy
    event_id = json_decoded['event_id']
    #event_id = 19

    # do the joiningz man
    rest_url='http://192.168.8.217:4180/api/event/attending/' + str(user_id) + '/'
    response = requests.request('PUT', rest_url, data={'event_id': event_id})

    response_json={"code": httplib.OK, "reason": "none", "info": response.text}
    return response_json

#Delete User to Event
@app.route('/deleteUserToEvent/', methods=['DELETE'])
def deleteUserToEvent():
    """
    Delete user to event
    Deletes a user from a certain event.
    Expects: user_id, event_id.

    ---
    tags:
      - User on Event
    responses:
      200:
        description: A single user item
        schema:
          id: return_json
          properties:
            code:
              type: integer
              description: The HTTP response code
              default: '200'
            reason:
              type: string
              description: The reason of user not being able to leave the event
              default: ''
    """
    # json_msg=web.data()
    json_decoded = json.loads(request.data)

    # get user id from joao
    user_id = json_decoded['user_id']
    # user_id = 1

    # get event id from johny boy
    event_id = json_decoded['event_id']
    #event_id = 19


    # do the deletingz man
    rest_url='http://192.168.8.217:4180/api/event/attending/' + str(user_id) + '/'
    response = requests.request('DELETE', rest_url, data={'event_id': event_id})
    response_json={"code": httplib.OK, "reason": "none", "info" : response.text}
    return response_json

#Get Users Near Event
@app.route('/getUsersNearEvent/', methods=['GET'])
def getUsersNearEvent():
    """
    Get users near event
    Gets all the users near an event and ordered by distance.
    Expects: event_id.

    ---
    tags:
      - User on Event
    responses:
      200:
        description: A single user item
        schema:
          id: return_test
          properties:
            code:
              type: integer
              description: The HTTP response code
              default: '200'
            info:
              type: string
              description: All the users info.
              default: 'e.g. http://pastebin.com/WUCFmedg'
    """


    # get event id from johny boy
    event_id = request.data
    # event_id = 19


    print event_id

    # get event from ivo san
    rest_url='http://192.168.8.217:4180/api/event/' + str(event_id) + '/'
    response = requests.get(rest_url)



    # get nearest users from ivo san
    event = json.loads(response.text)
    result = event['results'][0]
    longitude = result['location']['coordinates'][0]
    latitude = result['location']['coordinates'][1]
    interest = result['interest']['name']

    # do the deletingz man
    rest_url='http://192.168.8.217:4180/api/user/nearest/'
    response = requests.get(rest_url, {'longitude': longitude,
                                          'latitude': latitude,
                                          'interest': interest})

    response_json={"code": httplib.OK, "reason": "none", "info": response.text}
    return response_json



if __name__ == '__main__':
    app.run(port=8888, host="192.168.215.85")
