# -*- coding: utf-8 -*-
import json as json
from flask import Flask, request, redirect
import requests
import httplib
import json
import flask

app = Flask(__name__)

@app.route('/done/', methods=['POST'])
def done():
    json_get_users=json.loads(request.data)

    reg_ids=[]

    for user_id in json_get_users['results']:
        rest_url='http://192.168.215.85:5000/auth/api/users/' + user_id['id']
        response = requests.get(rest_url, data='')
        json=json.loads(response.text)
        reg_id=json['user']['regID']
        reg_ids+=[reg_id]

    return reg_ids


if __name__ == '__main__':
    app.run(port=8888, host="0.0.0.0", debug=True)