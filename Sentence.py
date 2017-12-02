class Sentence:
    __subject_carry_over = ['this', 'it', 'he', 'she', 'his', 'her']
    def __init__(self, words):
        self.words = words
        self.subject = None
        

    def print_sentence(self):
        for word in self.words:
            word.print_word()
        print('-----END OF SENTENCE-----')


    @staticmethod
    def update_subject(sentenceList):
        for sentence in sentenceList:
            firstWord = True
            previousSubject = None
            for word in sentence.words:
                if firstWord and word.content.lower() in Sentence.__subject_carry_over:
                    sentence.subject = previousSubject
                elif word.part_of_speech == 'NOUN':
                    sentence.subject = word.content
                firstWord = False
                previousSubject = sentence.subject
        return sentenceList

    @staticmethod
    def seperate_sentences(wordList):
        sentenceList = []
        sentence = []
        for word in wordList:
            if word.content == ".":
                sentenceObj = Sentence(sentence)
                sentenceList.append(sentenceObj)
                sentence = []
            else:
                sentence.append(word)
        return sentenceList


