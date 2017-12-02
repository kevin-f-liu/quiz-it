from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import re

from Word import Word


if __name__ == "__main__":
    client = language.LanguageServiceClient()
    text = u'The Golden Gate is in Bell High School. It is a cool Golden Gate Bridge'

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

    entityList.sort(key=lambda item: (-len(item.name), item.name))

    # replace the words with entities if possible
    # group together words appearing in the same entity
    matchIndices = []
    for entityContent in entityList:
        entityContentArr = entityContent.name.split(' ')
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
                # words.insert(i, entityContent)
                    #  replace this with actually creating a word object that has the appropriate attributes
                    # provided by entity (this means modifying the word object to be able to init a entity word)

    for word in words:
        # print(word.content)
        word.print_word()
    # print(wordsContentList)
    # print(matchIndices)
    # print(entity.mentions)
    # print( '/n')
    # for word in words:
    # 	print (word.content)
    # 	print (word.pos)
    # print('hellooooo')

