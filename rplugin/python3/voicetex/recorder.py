import logging
import sounddevice as sd
import soundfile as sf
import numpy as np
import os
from pydub import AudioSegment
import tempfile

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
        self.size_limit = 5 * 1024 * 1024  # 5MB

    def record(self, nvim, stop_key):
        if nvim is None:
            raise ValueError("Recorder must be called from within Neovim")

        self.recording = []  # Clear the current recording
        with sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=self.callback):
            nvim.command(f'echo "Recording... Press {stop_key} to stop."')
            nvim.command('let g:voicetex_recording_done = 0')
            nvim.command(f'nnoremap <silent> {stop_key} :let g:voicetex_recording_done = 1<CR>')
            while True:
                nvim.command('redraw')
                if nvim.eval('g:voicetex_recording_done'):
                    break
            nvim.command(f'nunmap {stop_key}')

        self.save_recording()
        if os.path.getsize(self.last_recording) > self.size_limit:
            nvim.command("echo 'Recording is too large. Please record again.'")
            os.remove(self.last_recording)
            self.last_recording = None
            return False
        return True

    def callback(self, indata, frames, time, status):
        if status:
            self.logger.error(status)
        self.recording.append(indata.copy())

    def save_recording(self):
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
            wav_file = temp_wav.name
            # Save as WAV
            sf.write(wav_file, np.concatenate(self.recording), self.samplerate)

        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_mp3:
            mp3_file = temp_mp3.name
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

    def cleanup(self):
        if self.last_recording and os.path.exists(self.last_recording):
            os.remove(self.last_recording)
            self.last_recording = None
            self.logger.info("Temporary recording file cleaned up")
