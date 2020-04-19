## Speech recognition module
This module is built based on two Google API：
- Cloud Speech-to-Text API
- Cloud Natural Language API
- Cloud Text-to-Speech API

API documentation：
- <https://cloud.google.com/speech-to-text/docs>
- <https://cloud.google.com/natural-language/docs>
- <https://cloud.google.com/text-to-speech/docs>

### Quick Start

1. To successfully test and run this module, you need to set up GCP.
    - go to <https://console.cloud.google.com>
    - Click "Select a project"
    - Set up a new project or use the project built before.
    - in the left menu go to API\& Services.
    - Search and enable “Cloud Natural Language API” and “Cloud Speech-to-Text API”.
    - Click “Credentials” => “Create credentials” => **“Service account key”** =>get your own **json** key.

2. Be sure to follow this page to set up the necessary Python environment.
    - <https://cloud.google.com/python/setup>    
    
3. Specific environments and quickstarts can be learned from official quickstarts pages:
    - <https://cloud.google.com/speech-to-text/docs/quickstart>
    - <https://cloud.google.com/natural-language/docs/quickstarts>
    - <https://cloud.google.com/text-to-speech/docs/quickstarts>

#### Installation
In this step, we assume you have finished all the necessary procedures given above.
Basic installation requirements are given in the .txt file, just run:

```
 pip3 install -r requirements.txt
```
for Python3.x.

##### PyAudio
Since this module is trying to get input from the microphone, you need to install PyAudio.
This process cannot be finished if you run **pip install** directly. Authors of another Python library
SpeechRecognition gives detailed description about the **PyAudio** module installation process:
- <https://github.com/Uberi/speech_recognition#pyaudio-for-microphone-users>

For those who want to use this module in the conda environment, just run this:
```
conda install nwani::portaudio nwani::pyaudio
```

It is based on this Reference:<https://github.com/ContinuumIO/anaconda-issues/issues/4139#issuecomment-433710003>

##### Playsound
To guarantee the program can get correct output speech voice based on the given
text(by the text-to-speech module), you need to install this package to play the 
.mp3 audio file. 

If you run this installation process in the conda environment just like me, then some 
**ModuleNotFoundError:No module named 'gi'** might be triggered. This problem can be solved by doing this:

Reference: <https://askubuntu.com/questions/1057832/how-to-install-gi-for-anaconda-python3-6?newreg=3a43e4aa13ff4b1f938afeac20da1fd9>

#### Features

- Transcribe audio from streaming input

    *single_utterance* is activated to enable the API to end the transcription request 
    immediately when it detects the end of speech. 
- Voice adaption

    use words listed in the *object.names* to improve the chance of being recognized by 
    the Speech-to-Text API. You can change the these feature phrases and the value of boost
    to attain a more acceptable result of your own program. 
- Multilingual recognition

    In this module, you can speak either Chinese or English to get the recognized result. While 
    the Chinese language cannot be dealt with in the following combination process. 
- Interaction of emotion

    1. To endow the robot with more practical interaction features, the Natural-Language API is enabled. 
    Then a threshold of **score** was carefully chosen to evaluate the mood of the current speaker.
    2. Some specific matches were established to pursue a more Intelligent interactive scene - with different object 
    labels, we can obtain different voice prompts.

#### Troubleshooting
Remember to adjust the input volume of the microphone to a normal level in case too much 
noise will lead to bad recognition results. You can use **test.py** to test whether your microphone 
is correctly working.

**Besides, make sure it is possible for you to use Google.**



    




