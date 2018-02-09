from language_constants import TAG_ENTITY, TAG_POS

class Word:
    """ Defines a word and all the relevant information relating to it from the api """

    def __init__(self, content, **kwargs):
        """ Create a word with optional configuration variables """
        self.content    = content
        self.entity     = kwargs.get('entity', None)
        self.salience   = kwargs.get('salience', 0)
        self.pos        = kwargs.get('pos', None)
        self.head_token = kwargs.get('head_token', None)
        self.number     = kwargs.get('number', None)
        self.person     = kwargs.get('person', None)
        self.gender     = kwargs.get('gender', None)
        
        self.blank = False # If blank, then the word comes up as _____ instead
        

    def print_word(self):
        print({"content": self.content, "part_of_speech": self.pos, "entity": self.entity,
               "salience": self.salience})

    def __str__(self):
        entity = 'NONE' if not self.entity else self.entity.name
        return '[{}|{}|{}|{}]'.format(self.content, entity, self.pos, self.person)

