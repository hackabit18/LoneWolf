import sqlite3
import json
import random
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer

config = RasaNLUModelConfig(configuration_values = {"pipeline":[{ "name": "nlp_spacy" },{ "name": "tokenizer_spacy" },
                                                   { "name": "intent_entity_featurizer_regex" },{ "name": "intent_featurizer_spacy"},
                                                   { "name": "ner_crf" },{ "name": "ner_synonyms" },{ "name": "intent_classifier_sklearn" },
                                                   { "name": "ner_spacy" }]})

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
    conn = sqlite3.connect("hotels.db")
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
    global response
    if intent=='greet':
        response = "Hello to you too!"
    if intent=='goodbye':
        if adr == '?' or adr == '':
            response = "Nice talking to you! Have fun!"
        else:
            response = "Nice talking to you! The address is {}! Have fun!".format(adr)
    return response

def respond(message, params, suggestions, excluded):
    print(message)
    parse_data = interpreter.parse(message)
    intent = parse_data["intent"]["name"]    
    entities = parse_data["entities"]
    if intent == "greet" or intent=="goodbye":
        global response, adr
        print(response)
        if 'Can I help you' in response:
            return 'Please specify some other choices!', '', {}, [], [], intent
        response = bot_answer(intent)
        return response, adr, {}, suggestions, [], intent
    if intent == "deny":
        global response
        if 'Can I help you' in response or 'Please specify' in response:
            return bot_answer('goodbye'), '', {}, suggestions, [], intent
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
    global params, suggestions, excluded, response, adr
    response, adr, params, suggestions, excluded, intent = respond(message, params, suggestions, excluded)
    return response, intent, suggestions
