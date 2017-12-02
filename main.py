from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import re

from Word import Word
from Sentence import Sentence

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
    text = u'The Golden Gate is in Bell High School. It is a cool Golden Gate Bridge.'

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    entities = client.analyze_entities(document).entities
    tokens = client.analyze_syntax(document).tokens

    words = []
    entityList = []

    # wordsContentList makes it easier to group words later on
    # basically the string content of the words
    wordsContentList = []

    # add word objects to Word list
    # add string content into wordsContentList
    for token in tokens:
        words.append(Word(token))
        wordsContentList.append(token.text.content)

    # includes all mentions in the entityList
    for entity in entities:
        for mention in entity.mentions:
            entity.name = mention.text.content
            entityList.append(entity)

    #sorts the entity list by length shortest to longest
    entityList.sort(key=lambda item: (-len(item.name), item.name))

    # replace the words with entities if possible
    # group together words appearing in the same entity
    matchIndices = []
    for entityContent in entityList:

        entityContentArr = entityContent.name.split(' ')
        # 
        for i in range(len(wordsContentList)):
            if i >= len(words):
                break
            if wordsContentList[i] == entityContentArr[0] \
                    and wordsContentList[i:i + len(entityContentArr)] == entityContentArr:
                del words[i + 1:i + len(entityContentArr)]
                words[i].add_entity(entityContent)
                wordsContentList[i] = entityContent.name
                for j in range(i+1, i+len(entityContentArr)):
                    wordsContentList[j] = 0

    sentenceList = Sentence.seperate_sentences(words)
    sentenceList = Sentence.update_subject(sentenceList)
    for sentence in sentenceList:
        sentence.print_sentence()

