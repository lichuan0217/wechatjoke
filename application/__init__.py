from flask import Flask, request, make_response
import hashlib
import xml.etree.ElementTree as etree
import time

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello NoCold-Joke"


@app.route("/wx", methods=['GET', ['POST']])
def wechat_auth():
    if request.methods == 'GET':
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
    # Get information from receive XML
    xml_recv = etree.fromstring(request.data)
    toUserName = xml_recv.find('ToUserName').text
    fromUserName = xml_recv.find('FromUserName').text
    content = xml_recv.find('Content').text.encode("utf-8")
    reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    response = make_response(reply % (fromUserName, toUserName,
                                      str(int(time.time())), content))
    response.content_type = "application/xml"
    return response
