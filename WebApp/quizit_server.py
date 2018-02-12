import os

from flask import Flask
from flask import request
from flask import render_template
from flask import make_response
import requests

from question_engine import QuestionEngine
from question import Question

QUIZLET_BASE_URL = 'https://api.quizlet.com/2.0/sets'

app = Flask(__name__) # Flask app
question_engine = QuestionEngine()

user_token = ""

@app.route('/', methods=['GET'])
def home():
    """ Get the main interface template """
    return render_template('home.html')


@app.route('/quiz', methods=['POST'])
def create_question_set():
    """ Create a question set based on the input text """
    if not user_token:
        # User must sign in first
        return

    quiz_title = request.args.get('quizlet_id', None)
    text = request.args.get('text_in', None)
    if not text or not quiz_title:
        # User must actually submit some text and an user id
        return

    questions = question_engine.generate_from_text(text)
    header = {'Authorization': 'Bearer ' + os.environ['QUIZLET_BEARER']}
    body = [
        ('title', name),
        ('lang_terms', 'en'),
        ('lang_definitions', 'en'),
    ] # Mandatory body parameters to post a new set

    for question in questions:
        sentence, answer = question.export()
        body.append((sentence, answer))
        
    r = requests.post(QUIZLET_BASE_URL, header=header, data=body)


@app.route('/quizletauth/', methods=['GET', 'POST'])
def quizlet_auth():
    """ Get both the authorization code and the bearer token """
    pass