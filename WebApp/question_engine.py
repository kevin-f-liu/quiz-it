from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from sentence import Sentence
from question import Question

class QuestionEngine:
    """ Main question generation engine """
    def __init__(self, **kwargs):
        """ Initialize question generator with configuration arguments
        Args:
            kwargs (Dict): Configuration options. TODO: Implement config
        """
        self.client = language.LanguageServiceClient() # Init client for API calls

        self.doc_type = kwargs.get('documentType', enums.Document.Type.PLAIN_TEXT)
        
    
    def generate_from_text(self, text):
        """ Entry point for inputting text, then converting to a problem set
        Args:
            text (String): Text (can be multiple sentences) that should be converted to questions
        Returns:
            questions (List[Question]): List of question objects created from text
        """
        sentences = self._get_sentences(text)
        sentences = Sentence.backreference_pronouns(sentences)
        questions = self._generate_questions(sentences)
        
        return questions


    def generate_from_image(self, url):
        """ Entry point for inputting image, then converting to a problem set
        Args:
            url (String): url of the image to be converted into text, and then to questions
        Returns:
            questions (List[Question]): List of question objects created from text
        """
        text = ""

        # TODO: Use google cloud vision to convert extract text from image
        # TODO: Sanitation and clean up of image text

        self.analyze_text(text)
    
    
    def _get_sentences(self, text):
        """ Create sentence objects from an input text
        Args:
            text (String): Input text to be converted to questions
        Returns:
            sentences (List[Sentence]): List of sentence objects created from text
        """
        document_syntax = self._get_syntax(text)
        response_sentences = [s for s in document_syntax.sentences]
        response_tokens = [t for t in document_syntax.tokens]
        response_sentences_tokens = self._group_tokens_to_sentences(response_sentences, response_tokens)

        sentences = []
        for idx, sentence in enumerate(response_sentences):
            response_sentence_entities = self._get_entities(sentence.text.content)
            sentences.append(Sentence(sentence.text.content, response_sentence_entities, response_sentences_tokens[idx]))

        return sentences
        
    
    def _group_tokens_to_sentences(self, sentences, tokens):
        """ Organizes the tokens into lists that mirror the actual text sentences
        Args:
            sentences (List): Google response sentences that should be formed with the tokens
            tokens (List): Google response tokens for each word in the origin text
        Returns: 
            List of Token Lists
        """
        sentences_tokens = []
        token_current = 0;
        for i in range(0, len(sentences)):
            next_sentence = []
            if i + 1 < len(sentences): 
                # Each sentence contains a start index, so the token that starts on that index is the start of a new sentence
                while tokens[token_current].text.begin_offset != sentences[i + 1].text.begin_offset:
                    tok = tokens[token_current]
                    next_sentence.append(tok)
                    token_current += 1
            else:
                # Add the last sentence which is the remaining tokens
                while token_current < len(tokens):
                    tok = tokens[token_current]
                    next_sentence.append(tok)
                    token_current += 1

            sentences_tokens.append(next_sentence)

        assert len(sentences) == len(sentences_tokens)
        return sentences_tokens


    def _generate_questions(self, sentences):
        """ Create questions from sentences containing entity and syntax info
        Args:
            sentences
        Returns:
            questions (List[Question]): List of question objects
        """
        return [Question(sentences) for sentences in sentences]


    def _get_entities(self, text):
        """ Api call to retrieve text entities """
        document = types.Document(
            content=text,
            type=self.doc_type
        )

        return self.client.analyze_entities(document=document, encoding_type="UTF32").entities

    def _get_syntax(self, text):
        """ Api call to retrive syntax analysis  """
        document = types.Document(
            content=text,
            type=self.doc_type,
        )

        return self.client.analyze_syntax(document=document, encoding_type="UTF32")