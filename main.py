from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import re

from Word import Word
from Sentence import Sentence
from Question import Question

# pip install pytesseract
# also get tesseract-ocr-setup-3.02.02.exe from https://sourceforge.net/projects/tesseract-ocr-alt/files/
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
# might need to change the path above

def GetTextFromImage(imagePath):
    return pytesseract.image_to_string(Image.open('imagePath'))


if __name__ == "__main__":
    client = language.LanguageServiceClient()
    text = u'Socrates was a philosopher who taught many young minds. \
            Socrates even taught Plato another great philosopher. \
            This great philosopher lived in the fifth century B.C. \
            Socrates was wrongly accused and sentenced to death, but his knowledge lives on. \
            Socrates was born around 470 B.C. Socrates was born into a poor family. \
            Socrates was born in a village on the side of Mount Lycabettus. \
            His father was a sculptor who was excellent at his job. When he was old enough his father taught \
            him how to be sculptor but his creations always came out less than acceptable in the eyes of the clients. \
            His mother was a mid wife. She helped deliver a lot of the children in Athens.'

    sentenceList = Sentence.seperate_sentences(text)
    sentenceList = Sentence.update_subject(sentenceList)

    questions = [Question(sentenceList) for sentenceList in sentenceList if Question.is_question(sentenceList)]
    for question in questions:
        print(question.export())

