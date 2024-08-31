import logging
import sounddevice as sd
import soundfile as sf
import numpy as np
import os
from pydub import AudioSegment

class Recorder:
    def __init__(self, samplerate=44100, channels=2):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

        self.samplerate = samplerate
        self.channels = channels
        self.recording = []
        self.last_recording = None
        self.folder = "recordings"
        self.filename = "output.mp3"
        self.temp_filename = "temp.wav"
        self.size_limit = 5 * 1024 * 1024  # 5MB

    def record(self, nvim):
        if nvim is None:
            raise ValueError("Recorder must be called from within Neovim")

        self.recording = []  # Clear the current recording
        with sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=self.callback):
            nvim.command('echo "Recording... Press Enter to stop."')
            nvim.command('let g:voicetex_recording_done = 0')
            nvim.command('nnoremap <CR> :let g:voicetex_recording_done = 1<CR>')
            while True:
                nvim.command('redraw')
                if nvim.eval('g:voicetex_recording_done'):
                    break
            nvim.command('nunmap <CR>')

        self.save_recording()
        self.last_recording = os.path.join(self.folder, self.filename)
        if os.path.getsize(self.last_recording) > self.size_limit:
            nvim.command("echo 'Recording is too large. Please record again.'")
            return False
        return True

    def callback(self, indata, frames, time, status):
        if status:
            self.logger.error(status)
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

        self.logger.info(f"Recording saved as {mp3_file}")
        self.last_recording = mp3_file

    def playback(self, nvim):
        if self.last_recording:
            self.logger.info(f"Playing back {self.last_recording}")
            data, samplerate = sf.read(self.last_recording)
            sd.play(data, samplerate)
            sd.wait()
        else:
            nvim.command("echo 'No recording available to play back.'")
