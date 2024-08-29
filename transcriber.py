import logging
from openai import OpenAI

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Transcriber:
    def __init__(self):
        self.client = OpenAI()

        self.temperature = 0.

        self.system_prompt = """
        You are a helpful assistant for a mathematician.
        Your task is to transform the following text into valid LaTeX code.
        In math mode,  words refer to macros and symbols.
        For example, "alpha" should be converted to "\alpha".
        """

    def transcribe_audio(self, audio_file_path):
        logging.info(f"Transcribing audio file: {audio_file_path}")
        with open(audio_file_path, 'rb') as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcription.text

    def postprocess_transcription(self, transcription):
        logging.info("Sending transcription to OpenAI for postprocessing")
        response = self.client.chat.completions.create(
            model="gpt-4o",
            temperature=self.temperature,
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": transcription
                }
            ]
        )
        return response.choices[0].message.content

    def transcribe(self, audio_file_path):
        transcription = self.transcribe_audio(audio_file_path)
        return self.postprocess_transcription(transcription)
