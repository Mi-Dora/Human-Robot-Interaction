from google.cloud import language_v1
from google.cloud.language_v1 import enums
from speech.text2speech import synthesize_text
import os


def sample_analyze_sentiment(text_content):
    """
    Analyzing Sentiment in a String
    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'I am so happy and joyful.'

    # [START language_python_migration_sentiment_text]
    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    # language = "en"
    document = {"content": text_content, "type": type_}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_sentiment(document, encoding_type=encoding_type)
    magnitude = response.document_sentiment.magnitude
    score = response.document_sentiment.score
    # Get overall sentiment of the input document
    # print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    # print(
    #     u"Document sentiment magnitude: {}".format(
    #         response.document_sentiment.magnitude
    #     )
    # )

    # adjust this two thresholds to get a better notice result
    if score < 0.4:
        print("Hey, man, what's up? Lift up your spirit! ")
        negative_notice = "Hey, man, what's up? Lift up your spirit! "
        synthesize_text(negative_notice, 7)
    # if magnitude < 0.000001:
    #     print("lift up your spirit! ")
    #     liftup_notice = "Hey, man, what's up? Lift up your spirit! "
    #     synthesize_text(liftup_notice, 8)
    # [END language_python_migration_sentiment_text]

    # Get sentiment for all sentences in the document

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))
