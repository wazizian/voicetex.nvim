"""Actual implement lies here."""
import pynvim as neovim
import pynvim.api
from .recorder import Recorder
from .transcriber import Transcriber
from .postprocessor import PostProcessor


@neovim.plugin
class VoiceTex:
    def __init__(self, nvim: pynvim.api.Nvim):
        self.nvim = nvim
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

    @neovim.command("ModuleHelloWorld")
    def hello_world(self) -> None:
        self.nvim.command("echom 'MyPlugin: Hello World!'")
