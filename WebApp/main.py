import json
import os

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import requests

from question_engine import QuestionEngine

QUIZLET_BASE_URL = 'https://api.quizlet.com/2.0/sets'


if __name__ == "__main__":
    text = 'Shopify was founded in 2004 by Tobias Lütke, Daniel Weinand, and Scott Lake after attempting to open Snowdevil, an online store for snowboarding equipment. Unsatisfied with the existing e-commerce products on the market, Lütke, a computer programmer by trade, instead built his own. Lütke used the open source web application framework Ruby on Rails to build Snowdevil\'s online store, and launched it after two months of development. The Snowdevil founders launched the platform as Shopify in June 2006. In June 2009, Shopify launched an API platform and App Store. The API allows developers to create applications for Shopify online stores and then sell them on the Shopify App Store. A Shopify window display in north London. In April 2010, Shopify launched a free mobile app on the Apple App Store. The app lets Shopify store owners view and manage their stores from iOS mobile devices. In 2010, Shopify started its Build-A-Business competition, in which participants create a business using its commerce platform. The winners of the competition receive cash prizes and mentorship from entrepreneurs, such as Richard Branson, Eric Ries and others. Shopify was named Ottawa’s Fastest Growing Company by the Ottawa Business Journal in 2010. The company received $7 million from an initial series A round of venture capital financing in December 2010. Its Series B round raised $15 million in October 2011.'
    quiz_title = "Shopify Quiz"


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
    r = requests.post(QUIZLET_BASE_URL, headers=header, data=body)
