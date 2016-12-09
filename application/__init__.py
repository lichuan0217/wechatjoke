from flask import Flask, request, make_response
import hashlib

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello NoCold-Joke"


@app.route("/wx", methods=['GET'])
def wechat_auth():
    token = "keepsecret"
    query = request.args
    signature = query.get('signature', '')
    timestamp = query.get('timestamp', '')
    nonce = query.get('nonce', '')
    echostr = query.get('echostr', '')
    s = [timestamp, nonce, token]
    s.sort()
    s = ''.join(s)
    if (hashlib.sha1(s).hexdigest() == signature):
        return make_response(echostr)
    return "Error"
