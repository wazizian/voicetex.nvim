import abc
import logging
from openai import OpenAI
import claudette

class PostProcessor(abc.ABC):
    @abc.abstractmethod
    def postprocess_transcription(self, transcription):
        pass

    @abc.abstractmethod
    def add_context(self, context):
        pass

    def add_context_from_files(self, *file_names):
        context = ""
        for file_name in file_names:
            with open(file_name, "r") as file:
                context += file.read()
        self.add_context(context)
        
    
class GPTPostProcessor(PostProcessor):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

        self.client = OpenAI()
        self.temperature = 0.

        self.system_prompt = """
        You are a helpful assistant for a mathematician.
        Your task is to transform the following text into valid LaTeX code.
        In math mode, words refer to macros and symbols.
        For example, "alpha" should be converted to "\alpha".

        Preferences:
        - Consider that you are in text mode by default.
        - Use the "amsmath" package.

        """
    
    def add_context(self, context):
        fcontext = f"""Follow closely the LaTeX code provided in the examples below.
        <EXAMPLES>
        {context}
        </EXAMPLES>"""
        self.system_prompt += fcontext

    def postprocess_transcription(self, transcription):
        self.logger.info("Sending transcription to OpenAI for postprocessing")
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
        self.logger.info(f"Postprocessed transcription: {response.choices[0].message.content}")
        self.logger.info(f"Usage: {response.usage}")
        return response.choices[0].message.content


class ClaudePostProcessor(PostProcessor):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

        self.model = claudette.models[1]
        self.logger.info(f"Using model: {self.model}")

        self.system_prompt = """
        You are a helpful assistant for a mathematician.
        Your task is to transform the following text into valid LaTeX code.
        In math mode, words refer to macros and symbols.
        For example, "alpha" should be converted to "\alpha".

        Preferences:
        - Consider that you are in text mode by default.
        - Use the "amsmath" package.

        """
        self.chat = claudette.Chat(self.model, sp=self.system_prompt)
    
    def add_context(self, context):
        fcontext = f"""Follow closely the LaTeX code provided in the examples below.
        <EXAMPLES>
        {context}
        </EXAMPLES>"""
        msg = claudette.mk_msg(fcontext, cache=True)

    def postprocess_transcription(self, transcription):
        self.logger.info("Sending transcription to Claude for postprocessing")
        response = self.chat(transcription)
        text = response.content[0]['text']
        self.logger.info(f"Postprocessed transcription: {text}")
        self.logger.info(f"Usage: {response.usage}")
        return text
