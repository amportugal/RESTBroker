import web
import json
import httplib
import requests
import urllib2
import urllib
from flask import request

paths = (
    '/user', 'User',
    '/event', 'Event',
    '/userOnEvent', 'UserEvent'
    '/login', 'Login'
)
app = web.application(paths, globals())

class User:

    #Register User
    def POST(self):

        #Obtain JSON from message
        json_msg=web.data()

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

    #Edit User
    def PUT(self):
        #Obtain JSON from message
        json_msg=web.data()

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

class Login:
    def GET(self):
        #Obtain JSON from message
        json_msg=web.data()

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


class Event:

    #Create event
    def POST(self, json_msg):

        #Obtain json message
        json_msg=web.data()

        #Location service: send event creation
        rest_url='http://192.168.8.217:4180/api/event'
        response = requests.GET(rest_url, json_msg)

        json_decoded=json.loads(response.text)

        if response.status_code!=httplib.CREATED:
            return response


        json_decoded=json.loads(json_msg)
        json_get_users={"latitude": json_decoded['latitude'], "longitude": json_decoded['longitude'], "interest": json_decoded['interest']}
        rest_url='http://192.168.8.217:4180/api/user/nearest&limit=' + json_decoded['min_people']
        response = requests.POST(rest_url, json_get_users)

        #TODO: extract users from response

        #TODO: Extract reg_ids from the json_msg to variable data_to_send
        #json_users=json.loads(response.text)

        #for user in json_users['results']:



        #Notification
        rest_url='http://192.168.8.217:4188/sendEventCreateNotification'
        r = requests.PUT(rest_url, data_to_send)

        response_json={"code": httplib.OK, "reason": "none"}

        return response_json

    #Edit event
    def PUT(self, json_msg):

        #Obtain json message
        json_msg=web.data()

        #Location service: send event creation
        rest_url='http://192.168.8.217:4180/api/event'
        response = requests.GET(rest_url, json_msg)

        json_decoded=json.loads(response.text)

        return response

    #Remove event
    def DELETE(self, json_msg):
        pass

    #Procurar evento
    def GET(self):
        pass

class UserEvent:

    #TODO: IVO
    #Join User to event
    def POST(self):
        pass

    #TODO: IVO
    #Delete user from event
    def DELETE(self):
        pass

    #TODO: IVO
    #Get users near event
    def GET(self):
        pass

class UserNFC:

    #NFC event attending
    def POST(self):
        pass

class RegisterPhone:

    #Register phone for notifications
    def POST(self):
        pass



if __name__ == "__main__":
    app.run()