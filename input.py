import os
import speech_recognition as sr

# This part of the code is responsible for capturing mic input and passing it back to the assistant for processing.

class InputHandler:
    def __init__(self, language, assist=None):
        if assist == None:
            # Initiate a fake assistant so this module can be tested and debugged independently of the main program.
            class MockAssistant(): running, talking, determineAction = True, False, None
            self.assistant = MockAssistant()
        else:
            self.assistant = assist

        self.r = sr.Recognizer()
        self.Running = True
        self.Language = language
    
    def listen(self):
        while self.Running and self.assistant.running:
            with sr.Microphone() as source:
                print("\033[31mListening...")
                audio = self.r.listen(source)

            try:
                print("\n\033[90mTranscribing..\033[0m")
                result = self.r.recognize_whisper(audio, language=self.Language)
                print(f"\033[1A\033[2K\033[0G{result}")
                if self.assistant.determineAction != None: self.assistant.determineAction(result)

            except sr.UnknownValueError:
                print("Whisper could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Whisper; {e}")

    def cleanup(self):
        print("\n\033[93mShutting down mic input...\033[0m")

def main():
    try:
        handler = InputHandler()
        handler.listen()
    except (KeyboardInterrupt, SystemExit): pass
    finally:
        handler.cleanup()

if __name__ == '__main__':
    main()