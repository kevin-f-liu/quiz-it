from copy import deepcopy

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from word import Word
from language_constants import TAG_ENTITY, TAG_GENDER, TAG_NUMBER, TAG_PERSON, TAG_POS, PRONOUNS

class Sentence:
    """ Holds data relevant to a sentence
    Params:
        text (String): The sentence in string form
        entity_list (List[GoogleAnalyzeEntitiesResponse]): Entities in the sentence, in order of appearance
        entity_reference (Dict): Quick lookup of entities by content
        tokens (List[GoogleAnalyzeSyntaxResponse]): Syntactual tokens in the sentence
        words (List[Word]): List of Word objects
        subject_major (Entity): Main subject of the sentence. Highest salience entity
        subject_minors (List[Entity]): Other words that are entities in the sentence
    """
    def __init__(self, text, entities, tokens):
        """ Initialize a sentence for question generation
        Args:
            text (String): String content of the sentence
            entities (List): Entities in the sentence
            tokens (List): Every word with analysis
        """
        self.text = text
        self.entity_list = None
        self.entity_reference = []
        self.tokens = []
        self.words = []

        self.subject_major = None
        self.subject_minors = []

        self._init_sentence_entities(entities)
        self._init_words(tokens)

        # print(entities)
        # print(self)
        # self.print_words()


    def _init_sentence_entities(self, entities):
        """ Initialize sentence entities
        Args:
            entities (Object): Aggregate of all entities in a sentence; returned by api 
        """

        # Create entity list and sorted entity list 
        entity_list = [e for e in entities]
        entity_list.sort(key=lambda item: item.mentions[0].text.begin_offset)
        entity_list_by_salience = list(entity_list)
        entity_list_by_salience.sort(key=lambda item: item.salience, reverse=True) # Most salient to least
        # Create entity hashmap
        entity_dict = {}
        for e in entities:
            entity_dict[e.name] = e

        if entities:
            # Create main subject
            subject_major = entity_list_by_salience[0]
            # Create minor subjects
            subject_minors = entity_list_by_salience[1:]
        else:
            subject_major = None
            subject_minors = []

        self.entity_reference = entity_dict
        self.entity_list = entity_list
        self.subject_major = subject_major
        self.subject_minors = subject_minors


    def _init_words(self, tokens):
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
        Raises:
            RuntimeException
        """
        if self.entity_list is None:
            raise RuntimeError("Entity list must be initialized first")
        
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
            word_entity_tag = self.entity_list[current_entity - 1].type if idx < current_word else None
            word_salience = self.entity_list[current_entity - 1].salience if idx < current_word else 0

            words.append(
                Word(
                    tok.text.content, 
                    entity=word_entity,
                    entity_tag=word_entity_tag,
                    salience=word_salience,
                    pos=tok.part_of_speech.tag, 
                    head_token=tok.dependency_edge.head_token_index,
                    number=tok.part_of_speech.number,
                    person=tok.part_of_speech.person,
                    proper=tok.part_of_speech.proper
            ))
        
        self.words = words


    def print_words(self):
        for w in self.words:
            print(str(w))


    def __str__(self):
        ret = ""
        for e in self.words:
            ret += e.get_content()
            ret += ' '
        return ret


    @staticmethod
    def update_subject(sentence_list):
        """ Given a list of sentences, replace pronouns with the subject of the sentence, or the one before. 
            Ex: "Elon Musk's car is midnight red. It is also fast." -> "Elon Musk's car is midnight red. The car is also fast."
        
        Args:
            sentence_list (List): list of sentences to modify
        """
        def _update_sentence_pronoun(sentence, pron, prev_sub):
            if not sentence.subject_major:
                sentence.subject_major = prev_sub
            else:
                sentence.subject_minors.append(prev_sub)

            pron.referenced_content = prev_sub.name
            pron.entity_tag = prev_sub.type
            pron.entity = prev_sub


        previous_subject = None
        previous_subject_minors = []
        for sentence in sentence_list:
            print()
            pronouns = [word for word in sentence.words if TAG_POS[word.pos] == 'PRON']
            entities = sentence.entity_list
            if not entities and not pronouns:
                # A sentence without entities and pronouns can't have questions asked about it
                sentence_list.remove(sentence)
                continue
            
            if pronouns:
                # Reference all pronouns to previous sentence
                # Generally, each pronoun matches exactly one subject in the previous sentence
                available_subjects = [previous_subject]
                available_subjects.extend(previous_subject_minors)
                for pron in pronouns:
                    if pron.get_content().lower() in PRONOUNS:
                        for prev_sub in available_subjects:
                            print(prev_sub.type)
                            if PRONOUNS[pron.get_content().lower()]['entity_tag'] == 'PERSON':
                                # Pronoun is a person
                                if TAG_ENTITY[prev_sub.type] == 'PERSON':
                                    available_subjects.remove(prev_sub)
                                    _update_sentence_pronoun(sentence, pron, prev_sub)
                                    break
                            elif pron.get_content().lower() == 'it' :
                                # Pronoun is generic
                                available_subjects.remove(prev_sub)
                                _update_sentence_pronoun(sentence, pron, prev_sub)
                                break
                

            if sentence.subject_major:
                # Sentence with a main subject can keep it.
                previous_subject = sentence.subject_major
                previous_subject_minors = sentence.subject_minors
                
        return sentence_list


if __name__ == "__main__":
    test = Sentence(u'the Golden Gate is in Bell High School')
