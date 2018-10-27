import re, pandas as pd, numpy as np
from flask import Flask, request, redirect
import requests
import sqlite3
import json
import random
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = "VERQNJNEKJNN*%$&8t47hxfcjksds"
PAGE_ACCESS_TOKEN = "EAAKYjSpIZBloBAP8l0MjwSIAYFPfiyqXxDuVx8ZCgNXJwEnmtYRMnFpd43hzGdCvag33NgncTSVFoBmhoYBSPHbvrTW5qNbheHS76ZAhZBahTgskZBS9UNSZCqwnTp7FthLEAsRr9K6uu8G70OD4Qa1fyxW2Q3m8f7TeNBvW7adzSuhHtePyzC"

config = RasaNLUModelConfig(configuration_values = {"pipeline":"spacy_sklearn"})
trainer = Trainer(config)
training_data = load_data("training_data.json")
interpreter = trainer.train(training_data)
response, adr, params, suggestions, excluded = '', '', {}, [], []

responses = ["I'm sorry...I couldn't find anything like that. Can I help you with anything else?",
"{} is a great place, don't you think so?",
"does {} sound good?",
"{} seems perfect for you, doesn't it?",
'how do you feel about {}?',
"I think {} would be a splendid choice, don't you?"
 ]

random.seed(0)
    
def find_hotels(params, excluded):
    # Open connection to DB    
    conn = sqlite3.connect("restaurants.db")
    # Create a cursor
    c = conn.cursor()
    # Create the base query
    query = 'SELECT * FROM restaurants'
    # Add filter clauses for each of the parameters
    if len(params) > 0:
        filters = ["{}=?".format(k) for k in params]
        print(filters)
        query += " WHERE " + " and ".join(filters)
    # Create the tuple of values
    t = tuple(params.values())
    print(query)
    # Execute the query
    c.execute(query,t)
    # Return the results
    data = list(c.fetchall())
    return data
    
def bot_answer(intent):
    if intent=='greet':
        response = "Hello to you too!"
    if intent=='goodbye':
        if adr == '?' or adr == '':
            response = "Nice talking to you! Have fun!"
        else:
            response = "Nice talking to you! The address is {}! Have fun!".format(adr)
    return response

def respond(message, params, suggestions, excluded):
    parse_data = interpreter.parse(message)
    intent = parse_data["intent"]["name"]    
    entities = parse_data["entities"]
    if intent == "greet" or intent=="goodbye":
        global response, adr
        if 'Can I help you' in response:
            return 'Please specify some other choices!', '', {}, [], [], intent
        response = bot_answer(intent)
        return response, adr, {}, [], [], intent
    if intent == "deny":
        global response
        if 'Can I help you' in response:
            return bot_answer('goodbye'), '', {}, [], [], intent
        excluded.extend(suggestions)
    for ent in entities:
        params[ent["entity"]] = str(ent["value"])
    print(params)
    results = find_hotels(params, excluded)
    names = [r[1] for r in results if r[1] not in excluded]
    address = [ r[2] for r in results if r[1] not in excluded]
    if len(names)==0:
        n = 0
    elif len(names)==1:
        n = 1
    else:
        n = random.randint(2,5)
    suggestions = names[:1]
    if suggestions:
        adr = address[:1][0]
    return responses[n].format(*suggestions), adr, params, suggestions, excluded, intent

def get_bot_response(message):
    #Call the respond function 
    global params, suggestions, excluded
    response, adr, params, suggestions, excluded, intent = respond(message, params, suggestions, excluded)
    params = params
    suggestions = suggestions
    return response, intent
