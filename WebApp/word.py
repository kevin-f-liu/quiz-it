from language_constants import TAG_ENTITY, TAG_POS

class Word:
    """ Defines a word and all the relevant information relating to it from the api """

    def __init__(self, content, **kwargs):
        """ Create a word with optional configuration variables """
        self._content    = content
        self.referenced_content = None
        self.entity     = kwargs.get('entity', None)
        self.salience   = kwargs.get('salience', 0)
        self.entity_tag = kwargs.get('entity_tag', None)
        self.pos        = kwargs.get('pos', None)
        self.head_token = kwargs.get('head_token', None)
        self.number     = kwargs.get('number', None)
        self.person     = kwargs.get('person', None)
        self.gender     = kwargs.get('gender', None)
        self.proper     = kwargs.get('proper', None)
        
        self.blank = False # If blank, then the word comes up as _____ instead

    def get_content(self):
        if self.blank:
            return '_____'

        return self.referenced_content if self.referenced_content else self._content
    
    def print_word(self):
        print({"content": self.get_content(), "part_of_speech": self.pos, "entity": self.entity,
               "salience": self.salience})

    def __str__(self):
        entity = 'NONE' if not self.entity else self.entity.name
        entity_tag = TAG_ENTITY[self.entity_tag] if self.entity_tag else "NONE"
        return '[{}|{}|{}|{}]'.format(self.get_content(), entity, TAG_POS[self.pos], entity_tag)

