# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 14:01:59 2023

@author: Casta
"""

import sqlite3
import requests
import os

def connect_db(db="chatbot.db"):
    # crear base de datos o conectar con ella si ya existe.
    try:
        return sqlite3.connect(db)
    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)


def create_tables():
    cnt = connect_db()
    cursor = cnt.cursor()
    # crear tabla usuario si no existe
    cursor.execute("""CREATE TABLE IF NOT EXISTS "usuarios" (
    "user_id"   INTEGER NOT NULL,
    "email" TEXT,
    "pass"  TEXT,
    PRIMARY KEY("user_id" AUTOINCREMENT))""")

def send_fb(email,password):
    
    client = EchoBot("<email>", "<password>")
    client.listen()

def get_users_by_id_fb(fb_id):
    cnt = connect_db()
    cursor = cnt.cursor()
    return cursor.execute("""SELECT * FROM usuarios WHERE fb_id=""",fb_id).fetchone()

def insert_user():

    try:
        cnt = connect_db()
        cursor = cnt.cursor()
        sentencia = "INSERT INTO usuarios(email, pass) VALUES (?,?)"
        cursor.execute(sentencia, ['chatbotprueba451@gmail.com','PruebaChatbot123456'])
        cnt.commit()
        print("Guardado correctamente")
    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)

def send_message(recipient_id, message):
    headers = {'Content-Type': 'application/json'}
    data = {
        'recipient': {'id': recipient_id},
        'message': {'text': message}
    }
    params = {'access_token': config.PAGE_ACCESS_TOKEN}
    response = requests.post(config.FB_API_URL,
                             headers=headers, params=params, json=data)
    return response.json()
    if response.status_code != 200:
        print('Error al enviar mensaje: {}'.format(response.text))

def verify_dir(route):

    directorio = route
    try:
        os.stat(directorio)
    except:
        os.mkdir(directorio)