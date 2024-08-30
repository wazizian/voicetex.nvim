import abc
import logging
import claudette

class PostProcessor(abc.ABC):
    @abc.abstractmethod
    def postprocess_transcription(self, transcription):
        pass

    @abc.abstractmethod
    def add_context(self, context):
        pass

    def add_context_from_buffers(self, buffers_names, buffers):
        context = ""
        for buffer_name, buffer in zip(buffers_names, buffers):
            context += f"<BUFFER {buffer_name}>\n{buffer}\n</BUFFER>\n"
        self.add_context(context)

    def add_context_from_files(self, *file_names):
        context = ""
        for file_name in file_names:
            with open(file_name, "r") as file:
                context += f"<FILE {file_name}>\n{file.read()}\n</FILE>\n"
        self.add_context(context)

class ClaudePostProcessor(PostProcessor):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

        self.model = claudette.models[1]
        self.logger.info(f"Using model: {self.model}")

        self.system_prompt = r"""
        You are a helpful assistant for a mathematician.
        Your task is to transform the following text into valid LaTeX code.
        In math mode, words refer to macros and symbols.
        For example, "alpha" should be converted to "\alpha".

        Preferences:
        - Consider that you are in text mode by default.
        - Do not include any preamble, \documentclass, \usepackage, or \begin{document}/\end{document} tags.
        - Output only the LaTeX code for the content itself.
        - Assume the amsmath package is available for use.
        - When the word "equation" is mentioned, use the equation environment (\begin{equation} ... \end{equation}).
        - When the word "align" is mentioned, use the equation environment (\begin{align} ... \end{align}).
        - For inline math, use $...$ delimiters.

        """
        self.chat = claudette.Chat(self.model, sp=self.system_prompt)
    
    def add_context(self, context):
        fcontext = f"""Take inspiration from the LaTeX code provided in the examples below.
        <EXAMPLES>
        {context}
        </EXAMPLES>"""
        msg = claudette.mk_msg(fcontext, cache=True)

    def postprocess_transcription(self, transcription, local_context=None):
        self.logger.info("Sending transcription to Claude for postprocessing")
        msg = ""
        if local_context:
            flocal_context = f"""Your answer will be inserted into the following context:
            <LOCAL_CONTEXT>
            {local_context[0]}
            <YOUR_ANSWER>
            {local_context[1]}
            </LOCAL_CONTEXT>\n"""
            msg += flocal_context
        msg += transcription
        response = self.chat(msg)
        latex_code = response.content[0].text.strip()
        
        self.logger.info(f"Postprocessed transcription: {latex_code}")
        self.logger.info(f"Usage: {response.usage}")
        return latex_code
