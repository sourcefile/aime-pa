# AI-Me: Your Personal Assistant
A human machine interface to assist in daily tasks. It is intended to be an offline / local alternative for the large AI agents currently being offered.

This project is mainly created as a pet project to understand the inner workings of larger AI applications, and get more familiar with Python as a C#.NET main. Because of this, code may not always be clean or conform to Python conventions

## Prerequisites
- Python (tested in 3.12)
- [Text generation WebUI](https://github.com/oobabooga/text-generation-webui/) in API mode. If you want to use a different (cloud) service, update the contents of the `getCompletion` function.

### Suggested models
- [MaziyarPanahi/Meta-Llama-3-8B-Instruct-GGUF](https://huggingface.co/MaziyarPanahi/Meta-Llama-3-8B-Instruct-GGUF): This works pretty decent on an old PC with a RTX 970. Not the fastest, but it gets the job done.

## Setup
```powershell
python -m venv venv\
.\venv\Scripts\activate
pip install torch==2.1.1+cu118 torchaudio==2.1.1+cu118 --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

After installation, create a `.env` in the root of the project. Here's a default config to get started. Adjust the settings as needed:

```
AI_NAME=AIme
USER_NAME=User
LLM_API_URI=http://127.0.0.1:5000/v1/chat/completions
COMPLETION_HISTORY_SIZE=10
VOICE_REFERENCE_FILE=Voice/reference.wav
AI_LANGUAGE=en
```

## Running the application
```powershell
py .\main.py
```

## How it works
The program consists of several parts. I try to split off as many parts into seperate module for easy swapping and isolated testing. Currently, the program contains the following modules:

- `main.py`: This module currently has two functions. First is the orchestration of all dependent modules used to run the AI. The second part is the decision-making logic which determines if the AI needs to take a specific action or simply chat with the user. Commands are given by starting a sentence with `Hey computer`. You can change the callsign for the AI by editing the `AiName` constant in the file. To see which commands are currently supported, check the command list further down.
- `input.py`: This module is intended to capture mic input and transcribe it into text for further processing. It relies on a local instance of [OpenAI Whisper](https://github.com/openai/whisper) for this translation. Whisper is wrapped inside [Speech Recognition](https://github.com/Uberi/speech_recognition/) to detect when the mic is in use and when the speaker is silent.
- `voice.py`: This module is intended to convert the reaction of the AI into speech. It uses [Coqui AI](https://github.com/idiap/coqui-ai-TTS) for this. After creating the audio, it is played using wave. Replace `Voice\reference.wav` to change the AI's voice.
- `mood.py`: This module is intended to interpret the mood of the AI's latest response. The intention is to have the avatar change based on the mood (once I get around to creat it). It uses [bhadresh-savani/distilbert-base-uncased-emotion](https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion?text=I+feel+a+bit+let+down) to determine the emotion.

### Commands
The AI currently supports the following commands:
- `terminate`: Shuts down the program

If a command is not recognized, the AI will automatically default to chatting with the user.

## To Do list
>*Why does this always get two new items every time I tick off one?*
- [x] Accept input from microphone and transcribe
- [x] Pass input into LLM and generate a response
- [x] Text-2-speech
  - [ ] Give it a better voice model and voice
- [x] Create personality prompt
- [x] Create logic to determine action
  - [ ] Search wiki
  - [ ] RAG / Document search
  - [ ] Current date and time
  - [x] Shutdown
  - [ ] Chat (if no other action seems appropriate)
  - [ ] (long-term): Replace search for specific words in prompt with intent recognition
- [x] Get settings from config file instead of hardcoded
- [ ] Virtual Avatar
- [ ] Emotions / Mood-recognition

## Sources
- [Livewhisper](https://github.com/Nikorasu/LiveWhisper): Sample python project used as a base for this project.
- [SchizoDev - My AI Girlfriend Got Even Better](https://www.youtube.com/watch?v=g0KMPpakuJc&ab_channel=SchizoDev): Used for leads on possible features to incorporate in this project