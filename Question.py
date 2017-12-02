from Sentence import Sentence
from Word import Word


class Question:
    __key_words = ('is', 'was', 'because', 'in', 'during', 'between')

    def __init__(self, sentence):
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
        return self.sentence.return_string(), self.answer.content

    @staticmethod
    def is_question(sentence):
        # gets list of all entities in the sentence
        entities = [word for word in sentence.words if word.entity]

        # gets all the words in the sentence as a list of strings
        words = sentence.return_string().split()

        if len(entities) == 0:
            return False

        # else
        for word in words:
            if word in Question.__key_words:
                return True


if __name__ == "__main__":
    tests = [Sentence(u'I love pancakes with banana'),
             Sentence(u'the mitochondria is the powerhouse of the cell'),
             Sentence(u'Socrates was a greek philosopher'),
             Sentence(u'he was a very important person')]
    Sentence.update_subject(tests)

    questions = [Question(test) for test in tests if Question.is_question(test)]
    for question in questions:
        print(question.export())

