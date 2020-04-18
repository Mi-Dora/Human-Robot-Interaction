from google.cloud import texttospeech
from playsound import playsound
import os


def synthesize_text(text, orderofsentence):
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.types.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Standard-C',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    with open("../Face_mic/output_audio/output{}.mp3".format(orderofsentence), 'wb') as out:
        out.write(response.audio_content)
        # print('Audio content written to file "output{}.mp3"'.format(orderofsentence))
        # play the .mp3 file
    playsound("../Face_mic/output_audio/output{}.mp3".format(orderofsentence))
# [END tts_synthesize_text]
