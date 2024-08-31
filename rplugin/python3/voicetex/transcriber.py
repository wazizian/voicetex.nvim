import logging
from openai import OpenAI


class Transcriber:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

        self.client = OpenAI()


    def transcribe_audio(self, audio_file_path):
        self.logger.info(f"Transcribing audio file: {audio_file_path}")
        with open(audio_file_path, 'rb') as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )
        text = transcription.text
        self.logger.info(f"Transcription: {text}")
        return text

    def transcribe(self, audio_file_path):
        return self.transcribe_audio(audio_file_path)
