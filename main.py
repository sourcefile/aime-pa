import requests
import os
from dotenv import load_dotenv
from input import InputHandler
from voice import VoiceOutput

# Config block
load_dotenv()
HistorySize = os.getenv("COMPLETION_HISTORY_SIZE")
AiName = os.getenv("AI_NAME")
UserName = os.getenv("USER_NAME")
LlmApiAddress = os.getenv("LLM_API_URI")
Language = os.getenv("AI_LANGUAGE")

Personality = f"""You are a personal AI assistant named {AiName}. You have fun helping users to get through their daily life.
You talk in a polite but informal way. You're not afraid to make the occasional snarky remark if the situation calls for it.
You try to answer questions in a friendly and concise way.

Use 'you' or '{UserName}' to refer to the individual asking the questions even if they ask with 'I'.
"""

class Assistant:
    def __init__(self, speaker):
        self.running = True
        self.talking = False
        self.history = []
        self.speaker = speaker

    def determineAction(self, input):
        cleanString = "".join(ch for ch in input if ch not in ",.?!'").lower()  # Removes punctuations Whisper adds
        query = cleanString.split()

        queried = cleanString[1:].startswith((AiName,"hey "+AiName,"okay "+AiName,"ok "+AiName))
        answer = ""
        if queried and "terminate" in query:
            self.running = False
            answer = self.getCompletion("Im done for now, see you later!")
        else:
            answer = self.getCompletion(input)
        
        print(answer) # TODO: Text-2-Speech
        self.speaker.speak(answer)

    def getCompletion(self, messageText):
        headers = {
            "Content-Type": "application/json"
        }
        self.history.append({"role": "user", "content": messageText})

        messages = []
        messages.append({"role": "system", "content": Personality})

        data = {
            "mode": "instruct",
            "messages": messages + self.history[~int(HistorySize):]
        }

        response = requests.post(LlmApiAddress, headers=headers, json=data, verify=False)
        assistant_message = response.json()['choices'][0]['message']
        self.history.append(assistant_message)
        return assistant_message['content']


def main():
    try:
        speaker = VoiceOutput(Language)
        pa = Assistant(speaker)
        handler = InputHandler(Language, pa)
        handler.listen()
    except (KeyboardInterrupt, SystemExit): pass
    finally:
        print("\n\033[93mQuitting..\033[0m")
        handler.cleanup()
        speaker.cleanup()

if __name__ == '__main__':
    main() 