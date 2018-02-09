from copy import deepcopy

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from word import Word
from language_constants import TAG_ENTITY, TAG_GENDER, TAG_NUMBER, TAG_PERSON, TAG_POS, _SUBJECT_CARRY_OVER

class Sentence:
    """ Holds data relevant to a sentence
    Params:
        text (String): The sentence in string form
        entity_list (List[GoogleAnalyzeEntitiesResponse]): Entities in the sentence
        entity_reference (Dict): Quick lookup of entities by content
        tokens (List[GoogleAnalyzeSyntaxResponse]): Syntactual tokens in the sentence
        words (List[Word]): List of Word objects
        subject_major (String): Main subject of the sentence. Generally the target of the root verb
        subject_minors (List[String]): Other words that are entities in the sentence

        __subject_carry_over (List[String]):
    """
    def __init__(self, text, entities, tokens):
        """ Initialize a sentence for question generation
        Args:
            text (String): String content of the sentence
            entities (List): Entities in the sentence
            tokens (List): Every word with analysis
        """
        self.text = text
        self.entity_list = self._create_entity_list(entities)
        self.entity_reference = self._create_entity_dict(entities)
        self.tokens = []
        self.words = self._create_words(tokens)

        self.subject_major = None
        self.subject_minors = []
        
        print(self)
        self.print_words()


    def _create_entity_list(self, entities):
        """ Convert API response aggregate type to list and sort"""
        entity_list = [e for e in entities]

        return entity_list


    def _create_entity_dict(self, entities):
        entity_dict = {}
        for e in entities:
            entity_dict[e.name] = e

        return entity_dict


    def _create_words(self, tokens):
        """ Create a list of words from a list of tokens 
            When finding the entity of a word, it's not enough to simply check if the entity contains the word.
            The word and all following words must fall into the same order as the entity.
            For example, in the sentence "The Statue of Liberty of New York is green", the first "of" should be 
            assigned the "Statue of Liberty" as an entity, but the second "of" should not. This is resolved
            by keeping two running pointers of the current entity (entity list will always be in order of appearance)
            and the current_word

            Args:
                tokens (List): List of tokens containing info to create the words
            Returns:
                List of Word instances
        """
        words = []

        current_entity = 0
        current_word = 0
        current_entity_words = []
        current_entity_words_pointer = 0

        for idx, tok in enumerate(tokens):
            # Add the entity that a word belongs in 
            if idx >= current_word and current_entity < len(self.entity_list):
                current_word = idx
                current_entity_words = self.entity_list[current_entity].name.split()
                while current_word < len(tokens) and current_entity_words_pointer < len(current_entity_words)\
                        and tokens[current_word].text.content == current_entity_words[current_entity_words_pointer]:
                    
                    current_entity_words_pointer += 1
                    current_word += 1
                # Done
                if current_entity_words_pointer == len(current_entity_words):
                    current_entity += 1
                    current_entity_words_pointer = 0
                else:
                    # Failed to find full entity name so reset to current
                    current_word = idx
            word_entity = self.entity_list[current_entity - 1] if idx < current_word else None

            words.append(
                Word(
                    tok.text.content, 
                    entity=word_entity,
                    pos=tok.part_of_speech.tag, 
                    head_token=tok.dependency_edge.head_token_index,
                    number=tok.part_of_speech.number,
                    person=tok.part_of_speech.person
            ))
        
        return words


    def print_words(self):
        for w in self.words:
            print(str(w))


    def __str__(self):
        ret = ""
        for e in self.words:
            ret += str(e)
            ret += ' '
        return ret


    @staticmethod
    def update_subject(sentence_list):
        previous_subject = None
        for sentence in sentence_list:
            nouns = [word for word in sentence.words if word.pos == 'NOUN' or word.pos == 'PRON']
            if not nouns:
                sentence_list.remove(sentence)
                continue
            if nouns[0].content.lower() in Sentence.__subject_carry_over:
                sentence.subject = previous_subject
                if previous_subject:
                    nouns[0].content = sentence.subject.content
                else:
                    sentence_list.remove(sentence)
            else:
                entities = [noun for noun in nouns if noun.entity]
                if not entities:
                    sentence_list.remove(sentence)
                    continue
                sentence.subject = entities[0]
                previous_subject = sentence.subject
        return sentence_list


if __name__ == "__main__":
    test = Sentence(u'the Golden Gate is in Bell High School')
