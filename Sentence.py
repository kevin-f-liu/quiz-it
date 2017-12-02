from Word import Word

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from copy import deepcopy


class Sentence:
    __subject_carry_over = ['this', 'it', 'he', 'she', 'his', 'her']

    def __init__(self, words):
        self.words = words
        self.subject = None

    def __str__(self):
        return self.return_string()

    def return_string(self):
        """
        :return: sentence in string format
        """
        return ' '.join([word.content for word in self.words])

    @staticmethod
    def update_subject(sentence_list):
        previous_subject = None
        for sentence in sentence_list:
            nouns = [word for word in sentence.words if word.part_of_speech == 'NOUN' or word.part_of_speech == 'PRON']
            if nouns[0].content.lower() in Sentence.__subject_carry_over:
                sentence.subject = previous_subject
                if previous_subject:
                    nouns[0].content = sentence.subject.content
                else:
                    sentence_list.remove(sentence)
            else:
                entity = [noun for noun in nouns if noun.entity][0]
                sentence.subject = entity
                previous_subject = sentence.subject
        return sentence_list

    @staticmethod
    def seperate_sentences(word_list):
        sentence_list = []
        sentence = []
        for word in word_list:
            if word.content == ".":
                sentence_obj = Sentence(sentence)
                sentence_list.append(sentence_obj)
                sentence = []
            else:
                sentence.append(word)
        return sentence_list


if __name__ == "__main__":
    test = Sentence(u'the Golden Gate is in Bell High School')
