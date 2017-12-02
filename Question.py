from Sentence import Sentence
from Word import Word
import copy


class Question:
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


if __name__ == "__main__":
    test = Sentence(u'the Golden Gate is in Bell High School')
    question = Question(test)
    question.sentence.print_sentence()
    print(question.answer)
