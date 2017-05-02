import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import requests
import json

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_question():
    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("Fiware")
def info_about_bio():
    url = "http://137.222.177.173:1026/v2/entities/air_pilot/attrs"

    headers = {
        'fiware-service': "uob",
        'fiware-servicepath': "/airquality"
    }

    response = requests.request("GET", url, headers=headers)
    # attributes_measured=""
    # for attribute in json.loads(response.text):
    #     attributes_measured = attribute+ " " + json.loads(response.text)[attribute]["value"]+ " "+ attributes_measured
    attributes_measured= "temperature %s degrees humidity %s carbon monoxide %s"%\
                         (json.loads(response.text)["TEMP"]["value"],json.loads(response.text)["HUM"]["value"],json.loads(response.text)["CO_PPM"]["value"])
    return question("The attributes measured are %s"% attributes_measured)


if __name__ == '__main__':
    app.run(debug=True)
