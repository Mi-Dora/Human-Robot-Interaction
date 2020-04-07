## Speech recognition module
This module is built based on two Google API：
- Cloud Speech-to-Text API
- Cloud Natural Language API

API documentation：
- <https://cloud.google.com/speech-to-text/docs>
- <https://cloud.google.com/natural-language/docs>

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

#### Installation
In this step, we assume you have finished all the necessary procedures given above.
Basic installation requirements are given in the .txt file, just run:

```
 pip3 install -r requirements.txt
```
for Python3.x.

Since this module is trying to get input from the microphone, you need to install PyAudio.
This process cannot be finished if you run **pip install** directly. Authors of another Python library
SpeechRecognition gives detailed description about the **PyAudio** module installation process:
- <https://github.com/Uberi/speech_recognition#pyaudio-for-microphone-users>

For those who want to use this module in the conda environment, just run this:
```
conda install nwani::portaudio nwani::pyaudio
```

It is based on this Reference:<https://github.com/ContinuumIO/anaconda-issues/issues/4139#issuecomment-433710003>

**Besides, make sure it is possible for you to use Google.**

#### Troubleshooting
Remember to adjust the input volume of the microphone to a normal level in case too much 
noise will lead to bad recognition results. You can use **test.py** to test whether your microphone 
is correctly working.




    




