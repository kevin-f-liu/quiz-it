import json

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from question_engine import QuestionEngine

if __name__ == "__main__":
    text = "Elon Musk flew a car into space. He is a god! Everyone should love Elon. This is going to be a weird sentence, so bear with me; I love weird sentences!"

    engine = QuestionEngine()

    engine.generate_from_text(text)
