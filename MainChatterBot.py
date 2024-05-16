# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 14:01:59 2023

@author: Casta
"""
# Descomente la siguiente línea para habilitar el registro detallado
import logging
logging.basicConfig(level=logging.CRITICAL)
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import common_functions
import config

userid="0"
def set_user(user_fb):
    userid = user_fb

common_functions.create_tables()
common_functions.verify_dir('./users/'+userid)
#common_functions.insert_user()
#user = common_functions.get_users()
#print(user)

"""
Este bot aprenderá respuestas basadas en una retroalimentación adicional
elemento del usuario.
"""

# Crear una nueva instancia de un ChatBot
bot = ChatBot(
    'Feedback Learning Bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///users/'+userid+'/db.sqlite3',   
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.LevenshteinDistance",
            #'default_response': 'No logro entenderte.',
            #'maximum_similarity_threshold': 0.60
        }
    ]

)
from chatterbot.trainers import ChatterBotCorpusTrainer
trainer = ChatterBotCorpusTrainer(bot)
Mytrainer = ListTrainer(bot)
trainer.train('./users/'+userid+'/train.yml')

def get_feedback(request,trainer):
    if trainer['stage'] == 1:
        if 'si' == request.lower():
            return {'response':False,'trainer':{'train':False,'request':trainer['request']}}
        elif 'no' == request.lower():
            return {'response':'¿Que deberia haber dicho?','trainer':{'train':True,'request':trainer['request'],'stage':2}}
        else:
            return {'response':'Por favor responda "Si" o "No"','trainer':{'train':True,'request':trainer['request'],'stage':1}}
    else:
        Mytrainer.train([str(trainer['request']),str(request)])
        return {'response':'\n He aprendido que cuando me pregunten {} debo responder {} \n Continua por favor.'.format(trainer['request'],request),'trainer':{'train':False,'request':trainer['request']}}

# El siguiente ciclo se ejecutará cada vez que el usuario ingrese la entrada
def response_bot(request,user_fb):

    set_user(user_fb)
    try:
        input_statement = Statement(request)
        response = bot.generate_response(input_statement)
        if config.TRAINER:
            if response.confidence < 0.8:
                return {'response':'\n "{}"\n\n ¿Fue la respuesta correcta?. \n Responde SI o NO'.format(response.text),'trainer':{'train':True,'request':request,'stage':1},'confidence':response.confidence}
            else:
                return {'response':response.text,'trainer':{'train':True,'request':False},'confidence':response.confidence}
        else:
            return {'response':response.text,'trainer':{'train':False,'request':False},'confidence':response.confidence}
    except Exception as e:
        return "Error inesperado:"+ str(e)