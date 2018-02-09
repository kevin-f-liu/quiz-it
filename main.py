from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import re

from Word import Word
from Sentence import Sentence
from Question import Question
# import vision

if __name__ == "__main__":
    client = language.LanguageServiceClient()
#     text = u'Socrates was a philosopher who taught many young minds. \
#             Socrates even taught Plato another great philosopher. \
#             This great philosopher lived in the fifth century B.C. \
#             Socrates was wrongly accused and sentenced to death, but his knowledge lives on. \
#             Socrates was born around 470 B.C. Socrates was born into a poor family. \
#             Socrates was born in a village on the side of Mount Lycabettus. \
#             His father was a sculptor who was excellent at his job. When he was old enough his father taught \
#             him how to be sculptor but his creations always came out less than acceptable in the eyes of the clients. \
#             His mother was a mid wife. She helped deliver a lot of the children in Athens.'
    text = "Linux was originally developed for personal computers based on the Intel x86 architecture, but has since been ported to more platforms than any other operating system. Because of the dominance of the Linux kernel-based Android OS on smartphones, Linux has the largest installed base of all general-purpose operating systems. Linux is also the leading operating system on servers and other big iron systems such as mainframe computers, and the only OS used on TOP500 supercomputers (since November 2017, having before gradually eliminated all competitors). It is used by around 2.3% of desktop computers."
    # text = vision.detect_document('picture.jpg')

    sentenceList = Sentence.seperate_sentences(text)
    sentenceList = Sentence.update_subject(sentenceList)

    questions = [Question(sentenceList) for sentenceList in sentenceList if Question.is_question(sentenceList)]
    for question in questions:
        print(question.export())

