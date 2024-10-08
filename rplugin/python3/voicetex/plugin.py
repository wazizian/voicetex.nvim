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

    @neovim.function("VoiceTexSetup", sync=True)
    def setup(self, args):
        """
        Set up the VoiceTex settings.

        :param args: List containing optional arguments, used to set the stop key
        """
        self.local_context_length = 5
        self.stop_key = args[0] if args and len(args) > 0 else '<CR>'
        return "Setup complete"

    def full_setup(self):
        """
        Set up the VoiceTex plugin components.
        """
        self.recorder = Recorder()
        self.transcriber = Transcriber()
        self.postprocessor = PostProcessor()

        # Fetch API keys from environment variables
        openai_api_key = os.getenv("OPENAI_API_KEY")
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

        if not openai_api_key or not anthropic_api_key:
            self.nvim.err_write('VoiceTex: API keys not found in environment. Please ensure OPENAI_API_KEY and ANTHROPIC_API_KEY are set.\n')
            exit(1)

        # Set environment variables for the Python process
        os.environ['OPENAI_API_KEY'] = openai_api_key
        os.environ['ANTHROPIC_API_KEY'] = anthropic_api_key

        self.nvim.out_write(f'VoiceTex: Set up! Stop key set to {self.stop_key}\n')
        return


    @neovim.command("VoiceTexContext", nargs='*')
    def add_context(self, args):
        """
        Add context files to the postprocessor.

        :param args: List of file names to be added as context
        """
        if not self.postprocessor:
            self.full_setup()

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
        if not all([self.recorder, self.transcriber, self.postprocessor]):
            self.full_setup()

        self.nvim.command("echo 'Recording... Press " + self.stop_key + " to stop.'")
        if self.recorder.record(self.nvim, self.stop_key):
            self.nvim.command("echo 'Recording stopped. Transcribing...'")
            
            try:
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
            finally:
                # Clean up the temporary recording file
                self.recorder.cleanup()
        else:
            self.nvim.command("echo 'Recording failed or was too large.'")
            self.recorder.cleanup()
