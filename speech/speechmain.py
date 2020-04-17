import linecache

from google.cloud import speech_v1p1beta1
from speech.emotion_analysis import sample_analyze_sentiment
from speech.text2speech import synthesize_text
from speech.speech2text import listen_print_loop
from speech.speech2text import ResumableMicrophoneStream
from speech.speech2text import STREAMING_LIMIT
from speech.speech2text import SAMPLE_RATE
from speech.speech2text import CHUNK_SIZE
from speech.speech2text import Finalresult
from speech.speech2text import YELLOW
import sys
import os
import cv2


def speak():
    """start bidirectional streaming from microphone input to speech API"""

    nameflag = 0
    real_name = 0
    objectflag = ""
    YES = False
    list_of_human = ["David", "Jordan", "Lebron"]
    client = speech_v1p1beta1.SpeechClient()
    enable_speaker_diarization = True

    # use the method of Voice adaptation in google-cloud speech to improve the accuracy of some
    # specific words, such as labels and names.
    phrases = ['Lebron', 'David', 'Jordan', 'cookies', 'crisps', 'instant_noodles',
               'mixed_congee', 'gum', 'canned_fruit', 'milk', 'water',
               'coffee', 'cola', 'herbal_tea', 'iced_tea', 'shampoo', 'soap',
               'toothpaste', 'napkin', 'slippers', 'floral_water', 'cup']

    # you can change the boost value to refactor the Voice adaptation effect
    boost = 10.0

    speech_contexts_element = {"phrases": phrases, "boost": boost}
    speech_contexts = [speech_contexts_element]

    # support different languages, you can change as you wish
    language_code = "zh"
    alternative_language_codes_element = "en"
    alternative_language_codes_element_2 = "es"
    alternative_language_codes = [
        alternative_language_codes_element,
        alternative_language_codes_element_2,
    ]

    config = speech_v1p1beta1.types.RecognitionConfig(
        encoding=speech_v1p1beta1.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        speech_contexts=speech_contexts,
        sample_rate_hertz=SAMPLE_RATE,
        enable_speaker_diarization=enable_speaker_diarization,
        language_code=language_code,
        alternative_language_codes=alternative_language_codes,
        max_alternatives=1)
    streaming_config = speech_v1p1beta1.types.StreamingRecognitionConfig(
        config=config,
        single_utterance=True,
    )

    mic_manager = ResumableMicrophoneStream(SAMPLE_RATE, CHUNK_SIZE)
    print(mic_manager.chunk_size)
    sys.stdout.write(YELLOW)
    # sys.stdout.write('\nListening, say "Quit" or "Exit" to stop.\n\n')
    sys.stdout.write('End (ms)       Transcript Results/Status\n')
    sys.stdout.write('=====================================================\n')

    LABEL_NUM = (len(open("../object/data/object.names", 'rU').readlines()))

    with mic_manager as stream:

        while not stream.closed:
            sys.stdout.write(YELLOW)
            sys.stdout.write('\n' + str(
                STREAMING_LIMIT * stream.restart_counter) + ': NEW REQUEST\n')

            stream.audio_input = []
            audio_generator = stream.generator()

            requests = (speech_v1p1beta1.types.StreamingRecognizeRequest(
                audio_content=content) for content in audio_generator)

            responses = client.streaming_recognize(streaming_config,
                                                   requests)

            # Now, put the transcription responses to use.
            listen_print_loop(responses, stream)

    Finalresult.pop()
    print(Finalresult)
    # Finalresult.pop()
    for i in range(len(Finalresult)):
        # apply the google-natural-language to attain a emotion analysis
        sample_analyze_sentiment(Finalresult[i])
        words = Finalresult[i].split(" ")
        wordslength = len(words)
        for word in range(wordslength):
            for name in range(3):
                if words[word] == list_of_human[name]:
                    nameflag = name + 1
                    real_name = words[word]
                    print(real_name)
                    YES = True
            for object_label in range(LABEL_NUM):
                line_content = linecache.getline("../object/data/object.names", object_label + 1)
                if words[word] == line_content.strip():
                    objectflag = line_content.strip()
                    print(objectflag)
                    YES = True

    return YES, nameflag, objectflag, real_name


if __name__ == '__main__':
    speak()
