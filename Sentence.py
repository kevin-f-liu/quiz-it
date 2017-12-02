from Word import Word

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


class Sentence:
    def __init__(self, text):
        client = language.LanguageServiceClient()

        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        entities = client.analyze_entities(document).entities
        tokens = client.analyze_syntax(document).tokens

        self.words = []
        entity_list = []

        # words_content_list makes it easier to group words later on
        # basically the string content of the words
        words_content_list = []

        # add word objects to Word list
        # add string content into words_content_list
        for token in tokens:
            self.words.append(Word(token))
            words_content_list.append(token.text.content)

        # includes all mentions in the entity_list
        for entity in entities:
            for mention in entity.mentions:
                entity.name = mention.text.content
                entity_list.append(entity)

        entity_list.sort(key=lambda item: (-len(item.name), item.name))

        # replace the words with entities if possible
        # group together words appearing in the same entity
        for entityContent in entity_list:
            entity_content_arr = entityContent.name.split(' ')
            for i in range(len(words_content_list)):
                if i >= len(self.words):
                    break
                if words_content_list[i] == entity_content_arr[0] \
                        and words_content_list[i:i + len(entity_content_arr)] == entity_content_arr:
                    del self.words[i + 1:i + len(entity_content_arr)]
                    self.words[i].add_entity(entityContent)
                    words_content_list[i] = entityContent.name
                    for j in range(i + 1, i + len(entity_content_arr)):
                        words_content_list[j] = 0
                        # words.insert(i, entityContent)
                        #  replace this with actually creating a word object that has the appropriate attributes
                        # provided by entity (this means modifying the word object to be able to init a entity word)

    def print_sentence(self):
        for word in self.words:
            print(word, end=' ')
        print()


if __name__ == "__main__":
    test = Sentence(u'the Golden Gate is in Bell High School')

    test.print_sentence()
