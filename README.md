# LoneWolf

# Restaurant Assistant

Our vision was to build a personal assistant who would locate and select the perfect place to eat for you based on your 
preferences. No need to look through the menus or the locations. No cause for checking your budget. No problems of looking up 
several sites and restaurant apps. We aimed to make this mundane process into an interactive and enjoyable one through our bot, 
the Restaurant Assistant.

You have to specify your choices like cuisine, budget, location in a personalized conversation and voila, you have the perfect 
place. And not just a single option, our assistant gives you several choices that are suited to your needs perfectly. And there’s 
no problem if you find something not to your liking with its first suggestion. You don’t have to open other pages to look for a 
restaurant as you would normally. You simply tell our assistant that this isn’t what you had in mind and it will get to work once 
again. Simply put, you can specify your preferences as well as things you do not want. You can talk to our assistant in a formal 
manner or in a casual way as well. We have included functionality so that our skill understands indirect requests such as 
“I am hungry” also. Our assistant will give you varied responses so that you feel like you are having an actual conversation 
instead of speaking with a bot.

Tools and Technologies: Python, RASA_NLU, Flask, HTML, CSS, Bootstrap, Alexa Skill Kit, AWS Lambda, Zulip API, ngrok

Steps:
1. Clone the repo.
2. Run the following commands to setup a virtual environment and install all requirements.
```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

Then go into the web_server folder and run the following commands:
```
export FLASK_APP=server.py
flask run
```

For running the zulip bot, go into zulip folder and run the following command:
```
python bot.py
```

For the messenger bot, go into facebook_messenger folder and run the following command:
```
export FLASK_APP=server.py
flask run
```
Also, run an ngrok https server and provide that link as a webhook on the facebook developer portal to make a messenger bot.

Some added features that we hope to implement in the near future would be multilingual service, because we wouldn’t want your 
experience to be limited. We also want to incorporate a large database with restaurants from various countries for customer 
satisfaction. Currently, our skill supports conversation in the English language and the database has restaurants in Mexico and
a few of BIT Mesra.

