# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 14:01:59 2023

@author: Casta
"""

from operator import truediv
from flask import Flask, request,render_template,jsonify
import common_functions
import config
from MainChatterBot import response_bot,get_feedback
import json

app = Flask(__name__)
app.debug = True

def verify_webhook(req):

    # Analizamos los parámetros de consulta
    mode = req.args.get('hub.mode')
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

    # Compruebe si hay un token y un modo en la cadena de consulta de la solicitud
    if mode and token:
        # Verifiquemos que el modo y el token enviado sean correctos
        if mode == "subscribe" and token == config.VERIFY_TOKEN:
            #Respondemos con '403 Prohibido' si los tokens de verificación no coinciden
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Si no coincide el token de verificacion y el modo.
            return "Forbidden", 403
    else:
        # Respuesta '400 Solicitud incorrecta' si el token o el modo no están en la cadena de consulta de la solicitud
        return "Bad Request", 400
    
res = {'train':False}
def respond(sender, message):
    """Formular una respuesta al usuario y
     pasarlo a una función que lo envía."""
    global res
    print(res) 
    if res['train'] and config.TRAINER:
        response = json.loads(json.dumps(get_feedback(message,res)))
    else:
        response = json.loads(json.dumps(response_bot(message,sender)))
    res = response['trainer']
    print(res)
    # common_functions.send_message(sender, response['response'])
    return response


def is_user_message(message):
    """Comprueba si el mensaje es de un usuario"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))

@app.route("/")
def index():
    return '<h1>Bienvenido a chatbot Facebook</h1>'

@app.route("/politica")
def politica():
    return render_template('politica.html')

@app.route("/webhook",methods=['GET'])
def webhook_get():
    return verify_webhook(request)
    
@app.route("/webhook",methods=['POST'])
def webhook_post():
    verify_webhook(request)
    payload = request.json
    event = payload['entry'][0]['messaging']
    for x in event:
        if is_user_message(x):
            text = x['message']['text']
            sender_id = x['sender']['id']
            respond = respond(sender_id, text)

    return respond

@app.route("/TestChatbot",methods=['POST'])
def TestChatbot():
    text = request.args.get('text')
    sender_id = request.args.get('id')
    return respond(sender_id, text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')