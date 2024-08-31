import pynvim as neovim
import pynvim.api
import os
from .recorder import Recorder
from .transcriber import Transcriber
from .postprocessor import PostProcessor


@neovim.plugin
class VoiceTex:
    """
    Main plugin class for VoiceTex, handling voice-to-LaTeX functionality in Neovim.
    """

    def __init__(self, nvim: pynvim.api.Nvim):
        """
        Initialize the VoiceTex plugin.

        :param nvim: Neovim instance
        """
        self.nvim = nvim
        self.local_context_length = 0
        self.recorder = None
        self.transcriber = None
        self.postprocessor = None
        self.stop_key = None

    @neovim.command("VoiceTexInit", nargs='?')
    def init(self, args=None) -> None:
        """
        Initialize the VoiceTex plugin components.

        :param args: Optional arguments, used to set the stop key
        """
        self.local_context_length = 5
        self.recorder = Recorder()
        self.transcriber = Transcriber()
        self.postprocessor = PostProcessor()
        self.stop_key = args[0] if args else '<CR>'

        # Fetch API keys from Lua's environment variables
        openai_api_key = self.nvim.exec_lua('return os.getenv("OPENAI_API_KEY")')
        anthropic_api_key = self.nvim.exec_lua('return os.getenv("ANTHROPIC_API_KEY")')

        if not openai_api_key or not anthropic_api_key:
            self.nvim.command("echoerr 'VoiceTex: API keys not found in environment. Please ensure OPENAI_API_KEY and ANTHROPIC_API_KEY are set.'")
            return

        # Set environment variables for the Python process
        os.environ['OPENAI_API_KEY'] = openai_api_key
        os.environ['ANTHROPIC_API_KEY'] = anthropic_api_key

        self.nvim.command(f"echom 'VoiceTex: Initialized! Stop key set to {self.stop_key}'")

    @neovim.command("VoiceTexContext", nargs='*')
    def add_context(self, args):
        """
        Add context files to the postprocessor.

        :param args: List of file names to be added as context
        """
        if not self.postprocessor:
            self.nvim.command("echoerr 'VoiceTex: Plugin not initialized. Run VoiceTexInit first.'")
            return

        cwd = self.nvim.call('getcwd')
        full_paths = [os.path.join(cwd, filename) for filename in args]
        existing_files = [path for path in full_paths if os.path.isfile(path)]

        if not existing_files:
            self.nvim.command("echo 'VoiceTex: No valid files provided as context.'")
            return

        self.postprocessor.add_context_from_files(*existing_files)
        self.nvim.command(f"echo 'VoiceTex: Added {len(existing_files)} file(s) as context.'")

    def get_local_context(self):
        """
        Get the local context around the cursor.

        :return: Tuple of (text before cursor, text after cursor)
        """
        buffer = self.nvim.current.buffer
        row, col = self.nvim.current.window.cursor
        
        start_row = max(0, row - self.local_context_length - 1)
        end_row = min(len(buffer), row + self.local_context_length)
        
        before_context = buffer[start_row:row-1]
        current_line_before = buffer[row-1][:col]
        current_line_after = buffer[row-1][col:]
        after_context = buffer[row:end_row]
        
        before = "\n".join(before_context + [current_line_before])
        after = "\n".join([current_line_after] + after_context)
        
        return (before, after)

    @neovim.command("VoiceTexRecord")
    def record_audio(self):
        """
        Record audio, transcribe it, postprocess into LaTeX, and insert at cursor position.
        """
        if not all([self.recorder, self.transcriber, self.postprocessor, self.stop_key]):
            self.nvim.command("echoerr 'VoiceTex: Plugin not initialized. Run VoiceTexInit first.'")
            return

        self.nvim.command("echo 'Recording... Press " + self.stop_key + " to stop.'")
        if self.recorder.record(self.nvim, self.stop_key):
            self.nvim.command("echo 'Recording stopped. Transcribing...'")
            
            # Transcribe the audio
            transcription = self.transcriber.transcribe(self.recorder.last_recording)
            
            # Get local context
            local_context = self.get_local_context()
            
            # Postprocess the transcription
            self.nvim.command("echo 'Postprocessing transcription...'")
            latex_code = self.postprocessor.postprocess_transcription(transcription, local_context)
            
            # Insert the LaTeX code at the cursor position
            self.nvim.command("normal! a" + latex_code)
            self.nvim.command("echo 'LaTeX code inserted.'")
        else:
            self.nvim.command("echo 'Recording failed or was too large.'")

    @neovim.command("ModuleHelloWorld")
    def hello_world(self) -> None:
        """
        A simple hello world command for testing purposes.
        """
        self.nvim.command("echom 'MyPlugin: Hello World!'")
