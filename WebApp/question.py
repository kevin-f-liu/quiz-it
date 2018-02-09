import requests

from bs4 import BeautifulSoup

from sentence import Sentence
from word import Word

class Question:
    """ Contains question generation logic """

    def __init__(self, sentence):
        """ Create a question from a sentence"""
        self.sentence = sentence
        self.answer = None

        self._create_question()

    def _create_question(self):
        answer = self.sentence.subject_major

        # replace the word being used as answer with a blank
        for word in self.sentence.words:
            if word.entity == answer:
                word.blank = True
        self.answer = answer

    def export(self):
        return str(self.sentence), self.answer.name
        

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

