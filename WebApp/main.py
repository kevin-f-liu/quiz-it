import json

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from question_engine import QuestionEngine

if __name__ == "__main__":
    text = u"My name is Julie and I am currently a second year student at the University of Waterloo School of Architecture.\
 My goal as an architecture student is to study and create immersive narrative spaces that highlight human moments, recall memories, and compel physical movement. Throughout my academic and professional career, I intend to explore how the built environment and the tangible experiences it creates can influence, and perhaps alter, our perception of the world."

    engine = QuestionEngine()

    questions = engine.generate_from_text(text)
    for question in questions:
        print(question.export())
