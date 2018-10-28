from flask import Flask, render_template, redirect, url_for
from logic import *

app = Flask(__name__)
FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = "VERQNJNEKJNN*%$&8t47hxfcjksds"
PAGE_ACCESS_TOKEN = "EAAKYjSpIZBloBAP8l0MjwSIAYFPfiyqXxDuVx8ZCgNXJwEnmtYRMnFpd43hzGdCvag33NgncTSVFoBmhoYBSPHbvrTW5qNbheHS76ZAhZBahTgskZBS9UNSZCqwnTp7FthLEAsRr9K6uu8G70OD4Qa1fyxW2Q3m8f7TeNBvW7adzSuhHtePyzC"


def verify_webhook(req):
    if req.args.get("hub.verify_token")==VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"
'''
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home Page')    
'''
'''
@app.route('/chat', methods=['GET','POST'])    
def chat():    
    user_message = UserMessageForm()
    if user_message.validate_on_submit():
        response, intent = get_bot_response(user_message.username)
        if intent == "goodbye":
            return redirect(url_for('/index'))
    return render_template('chat.html', title='Talk To Us', form=user_message)
'''

def respond(sender,message):
    response, intent = get_bot_response(message)
    send_message(sender,response)
    
def is_user_message(message):
    return (message.get('message') and message['message'].get('text') and not message['message'].get("is_echo"))
 
@app.route("/webhook",methods=['GET','POST'])
def listen():
    if request.method == 'GET':
        return verify_webhook(request)
    
    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id,text)
                
        return "ok"


def send_message(recipient_id, text):
    payload = {
        'message': {
             'text': text
        },
        'recipient': {
             'id': recipient_id
        },
        'notification_type': 'regular'
    }
    
    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }
    
    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )
    
    return response.json()
