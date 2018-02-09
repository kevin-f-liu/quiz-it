import requests

from bs4 import BeautifulSoup

from sentence import Sentence
from word import Word

class Question:
    """ Contains question generation logic """
    __key_words = ('is', 'was', 'because', 'in', 'during', 'between')

    def __init__(self, sentence):
        """ Create a question from a sentence"""
        self.sentence = sentence
        self.answer = self.generate_blank()

    def generate_blank(self):
        # sorts the words by highest salience first
        words = sorted(self.sentence.words, key=lambda x: x.salience, reverse=True)
        # keep only the words that are entities
        words = [word for word in words if word.entity]
        answer = words[0]
        # replace the word being used as answer with a blank
        for i, word in enumerate(self.sentence.words):
            if word == answer:
                self.sentence.words[i] = Word()
        return answer

    def export(self):
        return str(self.sentence), self.answer.content

    @staticmethod
    def is_question(sentence):
        # gets list of all entities in the sentence
        entities = [word for word in sentence.words if word.entity]

        # gets all the words in the sentence as a list of strings
        words = sentence.text.split()

        if len(entities) == 0:
            return False

        # else
        for word in words:
            if word in Question.__key_words:
                return True

    @staticmethod
    def get_wiki_questions(sentence):
        wiki_links = set([word.wiki for word in sentence.words if word.wiki and word.salience > 0.25])
        if len(wiki_links) == 0:
            return Question(sentence)
        soup = [BeautifulSoup(requests.get(link).text, "html.parser") for link in wiki_links]
        # either find the sentence using this soup object, or use the wikipedia api to get the first sentence
        wiki_sentences = Question(sentence)
        # replace sentence with a list of sentences from the wikis, plus the original sentence
        # the sentence from the wikipedia can be in the form of Entity: sentence, with the entity being blanked later on
        # make sure to convert the string sentence into a Sentence object
        return wiki_sentences


if __name__ == "__main__":
    tests = [Sentence(u'I love pancakes with banana'),
             Sentence(u'the mitochondria is the powerhouse of the cell'),
             Sentence(u'Socrates was a greek philosopher'),
             Sentence(u'he was a very important person')]
    Sentence.update_subject(tests)

    wiki = Question.get_wiki_questions(tests[2])
    questions = [Question(test) for test in tests if Question.is_question(test)]
    for question in questions:
        print(question.export())

