import os
import pyaudio
import torch
import wave
from TTS.api import TTS
from TTS.utils.synthesizer import Synthesizer

AudioOutputFile = "Voice/speak.wav"

class VoiceOutput:
    def __init__(self, language):
        print("Initializing Text-2-Speech module...")
        self.talking = False
        self.language = language
        print("Loading Voice model...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        print("Text-2-Speech module initialized.")

    def speak(self, inputString):
        self.model.tts_to_file(
            text = inputString,
            speaker_wav = "Voice/reference.wav",
            language = self.language,
            file_path = AudioOutputFile
        )

        # wav = self.model.tts(text = inputString, speaker_wav="reference.wav", language=self.language)
        wf = wave.open(AudioOutputFile, 'rb')

        # create an audio object
        p = pyaudio.PyAudio()
        stream = p.open(format =
                        p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True)
        data = wf.readframes(1024)

        while data:
            stream.write(data)
            data = wf.readframes(1024)
        wf.close()
        stream.close()    
        p.terminate()

        print("Done talking.")

    def cleanup(self):
        print("\n\033[93mCleaning up audio files...\033[0m")
        if os.path.exists(AudioOutputFile): os.remove(AudioOutputFile)

def main():
    try:
        speaker = VoiceOutput()
        speaker.speak("You should not be calling me directly...")
    except (KeyboardInterrupt, SystemExit): pass
    finally:
        speaker.cleanup()

if __name__ == '__main__':
    main()
