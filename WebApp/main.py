from googleapiclient.discovery import build
import json


if __name__ == "__main__":
    # Init natural language processing service with API key
    # API keys do not identify the user/application
    service = build('language', 'v1', developerKey='AIzaSyBcSxRU7-u2ietvX0XlkFW8KMblQMQx3w4')
    request = language.documents.annotateText(document="asdfasdf")