import sounddevice as sd
import soundfile as sf
import numpy as np
import os
import sys
from pydub import AudioSegment

class Recorder:
    def __init__(self, samplerate=44100, channels=2):
        self.samplerate = samplerate
        self.channels = channels
        self.recording = []
        self.last_recording = None
        self.folder = "recordings"
        self.filename = "output.mp3"
        self.temp_filename = "temp.wav"
        self.size_limit = 5 * 1024 * 1024  # 5MB

    def record(self):
        done = False
        while not done:
            self.recording = [] # Clear the current recording
            print("Recording... Press Enter to stop.")
            with sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=self.callback):
                input()  # Wait for the user to press Enter
            self.save_recording()
            self.last_recording = os.path.join(self.folder, self.filename)
            if os.path.getsize(self.last_recording) > self.size_limit:
                print("Recording is too large. Please record again.")
            else:
                done = True

    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.recording.append(indata.copy())

    def save_recording(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        wav_file = os.path.join(self.folder, self.temp_filename)
        mp3_file = os.path.join(self.folder, self.filename)

        # Save as WAV
        sf.write(wav_file, np.concatenate(self.recording), self.samplerate)

        # Convert to MP3
        audio = AudioSegment.from_wav(wav_file)
        audio.export(mp3_file, format="mp3")

        # Clean up temporary WAV file
        os.remove(wav_file)

        print(f"Recording saved as {mp3_file}")
        self.last_recording = mp3_file

    def playback(self):
        if self.last_recording:
            print(f"Playing back {self.last_recording}")
            data, samplerate = sf.read(self.last_recording)
            sd.play(data, samplerate)
            sd.wait()
        else:
            print("No recording available to play back.")
