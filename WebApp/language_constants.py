# Parts of speech
TAG_POS = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

# Entity types
TAG_ENTITY = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION', 'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

# Number of a word
TAG_NUMBER = ('SINGULAR', 'PLURAL', 'DUAL')

# Person 
TAG_PERSON = ('FIRST', 'SECOND', 'THIRD', 'REFLEXIVE_PERSON')

# Gender
TAG_GENDER = ('FEMININE', 'MASCULINE', 'NEUTER')

# Proper-ness
TAG_PROPER = ('PROPER', 'NOT_PROPER')

# Pronouns that can be easily replaced by a subject. Contains information on the number, person, and gender
PRONOUNS = {
    'it': {
        'entity_tag': 'ANY',
        'number': 'SINGULAR',
        'person': 'THIRD',
        'gender': 'NEUTER'
    }, 
    'he': {
        'entity_tag': 'PERSON',
        'number': 'SINGULAR',
        'person': 'THIRD',
        'gender': 'MASCULINE'
    }, 
    'she': {
        'entity_tag': 'PERSON',
        'number': 'SINGULAR',
        'person': 'THIRD',
        'gender': 'FEMININE'
    }, 
    'his': {
        'entity_tag': 'PERSON',
        'number': 'SINGULAR',
        'person': 'THIRD',
        'gender': 'MASCULINE'
    }, 
    'her': {
        'entity_tag': 'PERSON',
        'number': 'SINGULAR',
        'person': 'THIRD',
        'gender': 'FEMININE'
    }, 
    'they': {
        'entity_tag': 'ANY',
        'number': 'PLURAL',
        'person': 'THIRD',
        'gender': 'NEUTER'
    }, 
}

