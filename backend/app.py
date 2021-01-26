from os import path
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sslify import SSLify
import json

from utils import *
from usecases import *
from daos import UserDao

app = Flask(__name__)

CORS(app, supports_credentials=True)
sslify = SSLify(app)

@app.route('/', methods = ['GET', 'POST'])
def home_route():
    return 'Welcome To Edna One Endpoint'

@app.route('/init', methods = ['POST'])
def _edna():
    try:
        uid = verifyPOST(request)
        data = json.loads(request.data)
        filename = data['filename']

        load_data(uid, filename)

        return 'Good Request'
    except Exception as error:
        print(error)
        return 'Bad Request'

@app.route('/generate', methods = ['POST'])
def _generate():
    try:
        uid = verifyPOST(request)
        filePath = path.join(getTmpDir(), uid, 'WhatsApp', '_chat.csv')

        data = generate_all_data(uid, filePath)
        userDao = UserDao(uid)
        userDao.updateUser({
            'statistics': data
        })

        return data
    except Exception as error:
        print(error)
        return 'Bad Request'

@app.route('/getUserStatistics', methods = ['GET'])
def _get_statistic():
    try:
        uid = verifyPOST(request)
        return get_user_statistics(uid)
    except Exception as error:
        print(error)
        return 'Bad Request'

@app.route('/formatted/getData', methods = ['GET'])
def _get_formatted_data():
    # try:
    uid = verifyPOST(request)
    payload =  get_formatted_data(uid)
    return jsonify(payload)
    # except Exception as error:
    #     print(error)
    #     return 'Bad Request'

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(ssl_context="adhoc", host="0.0.0.0", port=5000)