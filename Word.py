class Word:
    def __init__(self, token):
        pos_tag = (
        'UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')
        self.content = token.text.content
        self.part_of_speech = pos_tag[token.part_of_speech.tag]
        self.entity = None
        self.salience = 0

    def add_entity(self, entity):
        entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                       'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
        self.entity = entity_type[entity.type]
        self.salience = entity.salience
        self.content = entity.name

    def print_word(self):
        print({"content": self.content, "part_of_speech": self.part_of_speech, "entity": self.entity,
               "salience": self.salience})

