# -*- coding: utf-8 -*-
from flask import Flask, request
import requests
import json
import flask

app = Flask(__name__)

@app.route('/done/', methods=['POST'])
def done():

    json_get_users=json.loads(request.data)

    reg_ids=[]

    for user_id in json_get_users['results']:
        rest_url='http://192.168.8.217:4150/auth/api/users/' + str(user_id['id'])
        response = requests.get(rest_url, data='')
        response_json=json.loads(response.text)
        reg_id=response_json['user']['regID']
        reg_ids+=[reg_id]


    return flask.jsonify(reg_ids=reg_ids)

if __name__ == '__main__':
    app.run(port=8888, host="localhost", debug=True)