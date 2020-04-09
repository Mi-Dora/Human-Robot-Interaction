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
from playsound import playsound
import os

os.environ['http_proxy'] = 'http://127.0.0.1:10809'
os.environ['https_proxy'] = 'http://127.0.0.1:10809'


def main():
    """start bidirectional streaming from microphone input to speech API"""

    client = speech_v1p1beta1.SpeechClient()
    enable_speaker_diarization = True

    # use the method of Voice adaptation in google-cloud speech to improve the accuracy of some
    # specific words, such as labels and names.
    phrases = ['red', 'yellow', 'blue', 'black', 'purple', 'white']

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
        interim_results=True)

    mic_manager = ResumableMicrophoneStream(SAMPLE_RATE, CHUNK_SIZE)
    print(mic_manager.chunk_size)
    sys.stdout.write(YELLOW)
    sys.stdout.write('\nListening, say "Quit" or "Exit" to stop.\n\n')
    sys.stdout.write('End (ms)       Transcript Results/Status\n')
    sys.stdout.write('=====================================================\n')

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

            if stream.result_end_time > 0:
                stream.final_request_end_time = stream.is_final_end_time
            stream.result_end_time = 0
            stream.last_audio_input = []
            stream.last_audio_input = stream.audio_input
            stream.audio_input = []
            stream.restart_counter = stream.restart_counter + 1

            if not stream.last_transcript_was_final:
                sys.stdout.write('\n')
            stream.new_stream = True
    print(Finalresult)
    Finalresult.pop()  # pop the final element since it will always be "exit" or "quit"

    # the Finalresult contains some sentences, we traverse them
    for i in range(len(Finalresult)):
        # apply the google-natural-language to attain a emotion analysis
        sample_analyze_sentiment(Finalresult[i])

        # in the next step, we will split all words in the previous text list
        words = Finalresult[i].split(" ")

        # if those feature words meet some specific requirements, then try to use the text2speech file
        """
        if words[k] == A:
            do 1
        elif words[k] == B:
            do 2
        """
        # this is the decision of output
        Robotresponse = "hello shaopu, wait for a moment"
        # use the method in google-text-to-speech systhesize a .mp3 audio file
        # then use the python package--Playsound read the content
        synthesize_text(Robotresponse, i)

        # play the audio file
        playsound("output{}.mp3".format(i))


if __name__ == '__main__':
    main()

# [END speech_transcribe_infinite_streaming]
