import pynvim as neovim
import pynvim.api
import os
from .recorder import Recorder
from .transcriber import Transcriber
from .postprocessor import PostProcessor


@neovim.plugin
class VoiceTex:
    def __init__(self, nvim: pynvim.api.Nvim):
        self.nvim = nvim
        self.local_context_length = 0
        self.recorder = None
        self.transcriber = None
        self.postprocessor = None

    @neovim.command("VoiceTexInit")
    def init(self) -> None:
        self.local_context_length = 5
        self.recorder = Recorder()
        self.transcriber = Transcriber()
        self.postprocessor = PostProcessor()
        self.nvim.command("echom 'VoiceTex: Initialized!'")

    @neovim.command("VoiceTexContext", nargs='*')
    def add_context(self, args):
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

    @neovim.command("VoiceTexRecord")
    def record_audio(self):
        if not self.recorder:
            self.nvim.command("echoerr 'VoiceTex: Plugin not initialized. Run VoiceTexInit first.'")
            return

        self.nvim.command("echo 'Recording... Press Enter to stop.'")
        self.recorder.record(self.nvim)
        self.nvim.command("echo 'Recording stopped.'")

    @neovim.command("ModuleHelloWorld")
    def hello_world(self) -> None:
        self.nvim.command("echom 'MyPlugin: Hello World!'")
