import json
import os

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import requests

from question_engine import QuestionEngine

QUIZLET_BASE_URL = 'https://api.quizlet.com/2.0/sets'


if __name__ == "__main__":
    text = u'Entrepreneur Elon Musk\'s first generation Tesla Roadster is an electric car that he selected as "something fun and without irreplaceable sentimental value" to be launched into space on the maiden flight of the Falcon Heavy rocket. It was launched on February 6, 2018 as part of the boilerplate, or dummy payload, on the Falcon Heavy Demonstration Mission. The car and rocket were both manufactured by companies founded or directed by Musk: the car was built by Tesla while the rocket was built by SpaceX. Musk\'s Roadster is the first consumer car sent into space, it had previously been used by Musk to commute to work around Los Angeles.\
The second stage with the car has sufficient velocity to escape the Earth and enter an elliptical heliocentric orbit that crosses the orbit of Mars, reaching an aphelion (maximum distance from the Sun) of 1.70 AU. During the early portion of its voyage it functioned as a broadcast device, sending live video back to Earth for slightly over four hours.'
    quiz_title = "Autogen Quiz2"


    question_engine = QuestionEngine()

    questions = question_engine.generate_from_text(text)
    header = {'Authorization': 'Bearer ' + os.environ['QUIZLET_BEARER']}
    body = [
        ('title', quiz_title),
        ('lang_terms', 'en'),
        ('lang_definitions', 'en'),
    ] # Mandatory body parameters to post a new set

    for question in questions:
        sentence, answer = question.export()
        body.append(('terms[]', sentence))
        body.append(('definitions[]', answer))
        
    print(body)
    # r = requests.post(QUIZLET_BASE_URL, headers=header, data=body)
