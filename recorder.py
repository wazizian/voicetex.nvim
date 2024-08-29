import sounddevice as sd
import soundfile as sf
import numpy as np
from pydub import AudioSegment
import os
import sys

class Recorder:
    def __init__(self, samplerate=44100, channels=2):
        self.samplerate = samplerate
        self.channels = channels
        self.recording = []

    def record(self):
        print("Recording... Press Enter to stop.")
        with sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=self.callback):
            input()  # Wait for the user to press Enter
        self.save_recording()

    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.recording.append(indata.copy())

    def save_recording(self, filename="output.mp3", folder="recordings"):
        if not os.path.exists(folder):
            os.makedirs(folder)
        wav_file = os.path.join(folder, "temp.wav")
        mp3_file = os.path.join(folder, filename)

        # Save as WAV
        sf.write(wav_file, np.concatenate(self.recording), self.samplerate)

        # Convert to MP3
        audio = AudioSegment.from_wav(wav_file)
        audio.export(mp3_file, format="mp3")

        # Clean up temporary WAV file
        os.remove(wav_file)

        print(f"Recording saved as {mp3_file}")
