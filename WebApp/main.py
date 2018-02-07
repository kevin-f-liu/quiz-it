from google.cloud import language
from google.cloud.language import enums
from google.could.language import types
import json


if __name__ == "__main__":
    # Init natural language processing service with API key
    # API keys do not identify the user/application
    # service = build('language', 'v1', developerKey='AIzaSyBcSxRU7-u2ietvX0XlkFW8KMblQMQx3w4')
    # request = language.documents.annotateText(document="asdfasdf")

    # Using Google Cloud Client Library
    client = language.LanguageServiceClient()
    