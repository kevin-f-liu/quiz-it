import json

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from question_engine import QuestionEngine

if __name__ == "__main__":
    text = "Mike was always an interesting kid. He would often get angry. Danny has a car. It is red and he likes to drive fast."

    engine = QuestionEngine()

    engine.generate_from_text(text)
