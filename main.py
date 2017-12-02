from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import re

from Word import Word
from Sentence import Sentence
from Question import Question

if __name__ == "__main__":
    client = language.LanguageServiceClient()
    text = u'Socrates was a philosopher who taught many young minds. Socrates even taught Plato another great philosopher. This great philosopher lived in the fifth century B.C. Socrates was wrongly accused and sentenced to death, but his knowledge lives on.  Socrates was born around 470 B.C. Socrates was born into a poor family. Socrates was born in a village on the side of Mount Lycabettus. His father was a sculptor who was excellent at his job. When he was old enough his father taught him how to be sculptor but his creations always came out less than acceptable in the eyes of the clients. His mother was a mid wife. She helped deliver a lot of the children in Athens.'

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

    questions = [Question(sentenceList) for sentenceList in sentenceList if Question.is_question(sentenceList)]
    for question in questions:
        print(question.export())

