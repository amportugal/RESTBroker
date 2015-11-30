# -*- coding: utf-8 -*-
from flask import Flask, request, redirect
from flasgger import Swagger
import requests
import httplib
import json
import flask

app = Flask(__name__)

Swagger(app)



@app.route('/registerRegId/', methods=['POST'])
def registerRegId():
    """
    Registers a registration id.
    Expects the following JSON:

    {
        "id": 20,
        "regID": "q3948y1r3hj31315qhjqwghqghvqwhjeqwv_qweqbqerurv3v1u"
    }


    ---
    tags:
      - User
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
            reason:
              type: string
              description: The reason of a not-created event
              default: ''
    """

    #Authentication service: Set Reg ID
    auth_rest_url='http://192.168.215.85:5000/auth/api/users/setRegID'
    response=requests.post(auth_rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"}, data=request.data)

    if response.status_code!=httplib.OK:
	 return flask.jsonify(code=response.status_code, reason="None")
    else:	
	 return flask.jsonify(code=httplib.OK, reason="None")


  

@app.route('/user/', methods=['POST'])
def userInfo():
    """
    Register or edits a user, if it exists.
    Expects the following JSON:

    {
        "id": 20,
        "latitude": 8,
        "longitude":9,
        "interests":["swag", "football", "fashion"]
    }


    ---
    tags:
      - User
    responses:
      200:
        description: A single user item
        schema:
          id: return_test
          properties:
            code:
              type: integer
              description: The HTTP response code
              default: '201'
            reason:
              type: string
              description: The reason of a not-created event
              default: ''
    """
    #Obtain JSON from message
    json_msg=request.data

    #Decode it
    json_decoded=json.loads(json_msg)

    #build new json message
    id=json_decoded['id']
    interests=json_decoded['interests']
    longitude=json_decoded['longitude']
    latitude=json_decoded['latitude']

    #json_decoded=json.loads(response.text)

    #Location service: GET user
    loc_rest_url='http://192.168.215.85:8000/api/user/' + id
    response=requests.get(loc_rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"}, data='')


    #If there is user, edit it
    if int(json_decoded['count'])!=0:
        loc_rest_url='http://192.168.215.85:8000/api/user/' + id
        code=httplib.OK
        json=flask.jsonify(id=id, longitude=longitude, latitude=latitude, interests=interests)
        response=requests.put(loc_rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"}, data=json)
        response_json = flask.jsonify(id=id, longitude=longitude, latitude=latitude, interests=interests)
    else:
        loc_rest_url='http://192.168.215.85:8000/api/user/'
        code=httplib.CREATED
        json=flask.jsonify(longitude=longitude, latitude=latitude, interests=interests)
        response=requests.post(loc_rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"}, data=json)


    response_json={"code": code, "reason": "none"}

    return response_json

@app.route('/user/', methods=['GET'])
def getUserInfo():
    """
    Get info about a user, if it exists.
    Expects user_id as query parameter.

    ---
    tags:
      - User
    responses:
      200:
        description: A single user item
        schema:
          id: return_test
          properties:
            code:
              type: integer
              description: The HTTP response code
              default: '201'
            info:
              type: string
              description: JSON with information about the user
              default: '
                {
                    "id": 3,
                    "location": {
                        "type": "Point",
                        "coordinates": [
                            -8.659602999691748,
                            40.6334416139116
                        ]
                    },
                    "interests": [
                        {
                            "id": 2,
                            "name": "football"
                        },
                        {
                            "id": 1,
                            "name": "party"
                        }
                    ],
                    "ranking": 0
                }
              '
    """
    #Obtain JSON from message
    user_id=request.args['user_id']

    #Location service: GET user
    loc_rest_url='http://192.168.215.85:8000/api/user/' + user_id
    response_loc=requests.get(loc_rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"}, data='')

    #Authentication service: GET user
    auth_rest_url='http://192.168.215.85:5000/auth/api/users/' + user_id
    response_auth=requests.get(auth_rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"}, data='')

    a_json=json.loads(response_loc.text)
    b_json=json.loads(response_auth.text)

    print b_json['user']
    data_to_send = {key: value for (key, value) in (a_json['results'][0].items() + b_json['user'].items())}

    return flask.jsonify(code=httplib.OK, info=data_to_send)


#Login
@app.route('/login/', methods=['GET'])
def loginPage():
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
    """

    return redirect("http://autheserv.ddns.net:4150/auth/api/users/login")

#Create Event: IT IS DONE, CHANGE STATIC DATA
@app.route('/event/', methods=['POST'])
def createEvent():
    """
    Create event
    Creates an event.
    Expects the following JSON:
    {
        "title": "New Event",
        "subtitle": "Subtitle of new event",
        "description": "Description of new event",
        "interest": 2,
        "latitude": 8.99309210,
        "longitude": 9.3019203,
        "host": 3,
        "attending": 3,
        "beginning": "2015-10-27T15:05:07Z",
        "end": "2015-10-29T15:05:07Z",
        "cost": 4,
        "type": "PUB",
        "min_people": 2,
        "max_people": 5,
        "image": "image/event_01.jpg"
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

    print request.data

    #Location service: send event creation
    rest_url='http://192.168.215.85:8000/api/event/'
    response = requests.post(rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"}, data=json_msg)

    if response.status_code!=httplib.OK:
        return str(response)

    event_id=response.text

    json_decoded=json.loads(json_msg)
    json_to_send={"latitude": json_decoded['latitude'], "longitude": json_decoded['longitude'], "interest": json_decoded['interest']}
    rest_url='http://192.168.215.85:8000/api/user/nearest/' + event_id + '?limit=' + str(json_decoded['min_people'])
    json_get_users = requests.get(rest_url, data=json_to_send)

    #Get event info
    rest_url='http://192.168.215.85:8000/api/event/' + event_id + '/'
    response_event = requests.get(rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"})

    a_json=json.loads(json_get_users.text)

    reg_ids=[]

    for user_id in a_json['results']:
        rest_url='http://192.168.215.85:5000/auth/api/users/' + str(user_id['id'])
        response = requests.get(rest_url, data='')
        response_json=json.loads(response.text)
        reg_id=response_json['user']['regID']
        reg_ids+=[reg_id]


    other_info={'event_id' : event_id, 'reg_ids' : reg_ids}

    data_to_send = {key: value for (key, value) in (other_info.items() + json.loads(response_event.text).items())}


    #Notification
    rest_url='http://localhost:8080/sendEventCreateNotification'

    r = requests.get(url=rest_url, data=json.dumps(data_to_send))
    response={"code": httplib.CREATED, "reason": "none", "event_id": int(event_id)}

    return str(response)

#Edit Event: IT IS DONE, CHANGE STATIC DATA
@app.route('/event/', methods=['PUT'])
def editEvent():
    """
    Edit event
    Edits an event.
    Expects the event_id as query parameter.
    Expects the following JSON:
    {
        "longitude": 1.234, (opcional)
        "latitude": 2.343, (opcional)
        "title": "title", (opcional)
        "subtitle": "subtitle", (opcional)
        "description": "event description", (opcional)
        "beginning": "2015-10-27T15:05:07Z", (opcional)
        "end": "2015-10-27T16:05:07Z", (opcional)
        "cost": 2, (opcional)
        "type": "PUB", (opcional)
        "min_people": 40, (opcional)
        "max_people": 100, (opcional)
        "interest": 2 (opcional)
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
    json_msg=request.data

    event_id=request.args['event_id']


    #Location service: send event creation
    rest_url='http://192.168.215.85:8000/api/event/' + event_id + "/"
    response = requests.put(rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"}, data=json_msg)

    print response.text
    if response.status_code!=httplib.OK:
        return str(response)


    rest_url='http://192.168.215.85:8000/api/user/attending/event/' + event_id + "/"
    json_get_users = requests.get(rest_url, "")

    #Get event info
    rest_url='http://192.168.215.85:8000/api/event/' + event_id + '/'
    response_event = requests.get(rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"})

    a_json=json.loads(json_get_users.text)

    #Initialize
    reg_ids=[]

    for user_id in a_json['results']:
        rest_url='http://192.168.215.85:5000/auth/api/users/' + str(user_id['id'])
        response = requests.get(rest_url, data='')
        response_json=json.loads(response.text)
        reg_id=response_json['user']['regID']
        reg_ids+=[reg_id]

    other_info={'event_id' : event_id, 'reg_ids' : reg_ids}

    data_to_send = {key: value for (key, value) in (other_info.items() + json.loads(response_event.text).items())}


    #Notification
    rest_url='http://localhost:8080/sendEventUpdateNotification'
    r = requests.get(url=rest_url, data=json.dumps(data_to_send))

    response_json={"code": httplib.OK, "reason": "none"}

    return str(response_json)

#Delete Event: IT IS DONE, CHANGE STATIC DATA
@app.route('/event/', methods=['DELETE'])
def deleteEvent():
    """
    Delete event
    Delete an event.
    Expects the event_id as query parameter.

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
    event_id=request.args['event_id']

    #Get event info
    rest_url='http://192.168.215.85:8000/api/event/' + event_id + '/'
    response_event = requests.get(rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"})

    #Location service: send event deletion
    rest_url='http://192.168.215.85:8000/api/event/' + event_id + "/"
    response = requests.delete(rest_url,  headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"})


    if response.status_code!=httplib.OK:
        return str(response)


    rest_url='http://192.168.215.85:8000/api/user/attending/event/' + event_id + "/"
    json_get_users = requests.get(rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"})


    a_json=json.loads(json_get_users.text)

    #Initialize
    reg_ids=[]

    for user_id in a_json['results']:
        rest_url='http://192.168.215.85:5000/auth/api/users/' + str(user_id['id'])
        response = requests.get(rest_url, data='')
        response_json=json.loads(response.text)
        reg_id=response_json['user']['regID']
        reg_ids+=[reg_id]

    other_info={'event_id' : event_id, 'reg_ids' : reg_ids}

    data_to_send = {key: value for (key, value) in (other_info.items() + json.loads(response_event.text).items())}

    #Notification
    rest_url='http://localhost:8080/sendEventDeletionNotification'
    r = requests.get(url=rest_url, data=json.dumps(data_to_send))

    response_json={"code": httplib.CREATED, "reason": "none"}

    return str(response_json)

#Search Event: IT IS DONE
@app.route('/event/', methods=['GET'])
def searchEvent():
    """
    Search for event
    Searches for an event.
    Expects the event_id as query parameter.

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
    event_id=request.args['event_id']

    #Location service: get event
    rest_url='http://192.168.215.85:8000/api/event/' + event_id + '/'
    response = requests.get(rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"})

    if response.status_code!=httplib.OK:
        return str(response)

    json_result=json.loads(response.text)

    if not json_result['results']:
        response_json={"code": httplib.OK, "reason": "No event has been found", "info": ""}
    else:
        response_json={"code": httplib.OK, "reason": "none", "info": response.text}

    return str(response_json)


#Get Nearest Events: IT IS DONE
@app.route('/getNearestEvents/', methods=['GET'])
def getNearestEvents():
    """
    Get Nearest events
    Obtains all the events near the user.
    Expects the user_id as query parameter.

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
    #user_id=request.args['user_id']
    user_id=3

    #Location service: send event creation
    rest_url='http://192.168.215.85:8000/api/event/nearest/' + str(user_id) + '/?format=json'

    response = requests.get(rest_url)


    if response.status_code!=httplib.OK:
        return str(response)

    #response_json={"code": httplib.OK, "reason": "none", "info": json.loads(str(response.text))}


    #return str(response_json)
    return flask.jsonify(code=httplib.OK,
                   reason="none",
                   info=json.loads(response.text))



#Join User to Event: IT IS DONE
@app.route('/joinUserToEvent/', methods=['POST'])
def joinUserToEvent():
    """
    Join user to event
    Joins a user to a certain event.
    Expects user_id and event_id as query parameters.

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

    # get user id from joao
    user_id = request.args['user_id']
    #user_id = 1

    # get event id from johny boy
    event_id = request.args['event_id']
    #event_id = 19

    # do the joiningz man
    rest_url='http://192.168.215.85:8000/api/event/attending/' + str(user_id) + '/'
    response = requests.request('PUT', rest_url, data={'event_id': event_id})

    if response.status_code!=httplib.OK:
        return str(response)

    response_json={"code": httplib.OK, "reason": "none", "info": response.text}


    #Get event info
    rest_url='http://192.168.215.85:8000/api/event/' + event_id + '/'
    response_event = requests.get(rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"})

    #Notification
    #rest_url='http://192.168.215.85:8000/api/user/host/event/' + event_id + "/"
    #json_get_users = requests.get(rest_url, headers={"X-CSRFToken": "04cAmRuBNouFtoq6ZkXcqq7cVKXiW5rH", "Content-type" : "application/json"})

    #a_json=json.loads(json_get_users.text)['results']


    #rest_url='http://192.168.215.85:5000/auth/api/users/' + str(a_json[0]['id'])
    #response = requests.get(rest_url, data='')
    #response_json=json.loads(response.text)
    #reg_id=response_json['user']['regID']

    #other_info={'event_id' : event_id, 'reg_ids' : reg_id, 'new_user': user_id}

    #data_to_send = {key: value for (key, value) in (other_info.items() + json.loads(response_event.text).items())}

    #Notification
    #rest_url='http://localhost:8080/sendEventJoinNotification'
    #r = requests.get(url=rest_url, data=json.dumps(data_to_send))

    return flask.jsonify(code=httplib.OK, reason="None")

#Delete User to Event: IT IS DONE
@app.route('/deleteUserToEvent/', methods=['DELETE'])
def deleteUserToEvent():
    """
    Delete user to event
    Deletes a user from a certain event.
    Expects user_id and event_id as query parameters.

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
    #json_decoded = json.loads(request.data)

    # get user id from joao
    user_id = request.args['user_id']

    # get event id from johny boy
    event_id = request.args['event_id']


    # do the deletingz man
    rest_url='http://192.168.215.85:8000/api/event/attending/' + str(user_id) + '/'
    response = requests.request('DELETE', rest_url, data={'event_id': event_id})

    if response.status_code!=httplib.OK:
        return str(response)

    response_json={"code": httplib.OK, "reason": "none", "info" : response.text}

    return str(response_json)

#Get Users Near Event: NOT WORKING
@app.route('/getUsersNearEvent/', methods=['GET'])
def getUsersNearEvent():
    """
    Get users near event
    Gets all the users near an event and ordered by distance.
    Expects event_id as query parameter.

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
    event_id = request.args['event_id']


    # # get event from ivo san
    # rest_url='http://192.168.215.85:8000/api/event/' + str(event_id) + '/'
    # response = requests.get(rest_url)
    #
    # if response.status_code!=httplib.OK:
    #     return str(response)
    #
    # # get nearest users from ivo san
    # event = json.loads(response.text)
    # result = event['results'][0]
    # longitude = result['location']['coordinates'][0]
    # latitude = result['location']['coordinates'][1]
    # interest = result['interest']['name']

    # do the deletingz man
    rest_url='http://192.168.215.85:8000/api/user/nearest/' + str(event_id)
    response = requests.get(rest_url)

    if response.status_code!=httplib.OK:
        return str(response)

    response_json={"code": httplib.OK, "reason": "none", "info": response.text}

    return str(response_json)

@app.route('/getUserAttendingEvents/', methods=['GET'])
def getUserAttendingEvents():
    """
    Get all the events a user attends
    Gets all the events a user attends
    Expects user_id as query parameter.

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
    user_id = 3#request.args['user_id']

    # do the deletingz man
    rest_url='http://192.168.215.85:8000/api/event/attending/' + str(user_id)
    response = requests.get(rest_url)

    if response.status_code!=httplib.OK:
        return str(response)

    return flask.jsonify(code=httplib.OK,
                   reason="none",
                   info=json.loads(response.text))

@app.route('/getUserHostingEvents/', methods=['GET'])
def getUserHostingEvents():
    """
    Get all the events a user attends
    Gets all the events a user attends (even if host)
    Expects user_id as query parameter.

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
    user_id = 3#request.args['user_id']

    # do the deletingz man
    rest_url='http://192.168.215.85:8000/api/event/attending/' + str(user_id)
    response = requests.get(rest_url)

    if response.status_code!=httplib.OK:
        return str(response)

    return flask.jsonify(code=httplib.OK,
                   reason="none",
                   info=json.loads(response.text))



@app.route('/getUserHostEvents/', methods=['GET'])
def getUserHostEvents():
    """
    Get all events a user hosts
    Gets all the events a user hosts
    Expects user_id as query parameter.

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
    user_id = 3#request.args['user_id']

    # do the deletingz man
    rest_url='http://192.168.215.85:8000/api/event/host/' + str(user_id)
    response = requests.get(rest_url)

    if response.status_code!=httplib.OK:
        return str(response)

    return flask.jsonify(code=httplib.OK,
                   reason="none",
                   info=json.loads(response.text))



if __name__ == '__main__':
    app.run(port=8888, host="192.168.215.85", debug=True)
