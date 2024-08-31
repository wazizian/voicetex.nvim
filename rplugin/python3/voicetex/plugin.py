"""Actual implement lies here."""
import pynvim as neovim
import pynvim.api


@neovim.plugin
class VoiceTex:
    def __init__(self, nvim: pynvim.api.Nvim):
        self.nvim = nvim

    @neovim.command("VoiceTexInit")
    def init(self) -> None:
        self.local_context_length = 5
        self.nvim.command("echom 'MyPlugin: Initialized!'")

    @neovim.command("ModuleHelloWorld")
    def hello_world(self) -> None:
        self.nvim.command("echom 'MyPlugin: Hello World!'")
