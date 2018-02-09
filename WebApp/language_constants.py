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

# 
_SUBJECT_CARRY_OVER = ['this', 'it', 'he', 'she', 'his', 'her']