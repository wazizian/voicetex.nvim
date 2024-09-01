# VoiceTex

VoiceTex is a Neovim plugin that enables voice-to-LaTeX functionality, allowing users to dictate mathematical content directly into their documents. It provides a seamless integration of speech recognition and LaTeX formatting within the Neovim environment.

On a more personal note: I wrote this when I injured my dominant arm and I could not write with it anymore. This plugin was  written with [aider](https://github.com/paul-gauthier/aider) which was of great help given my situation.

## Features

- Audio recording and transcription
- Conversion of transcribed text to LaTeX code
- Context-aware LaTeX generation
- Integration with local document context

## Installation

### Dependencies

Ensure you have the following prerequisites:

- Neovim (0.5.0 or later)
- Python 3.6 or later
- OpenAI API key (for transcription using Whisper model)
- Anthropic API key (for LaTeX conversion using Claude model)

Install the required Python packages:

```bash
pip install pynvim openai sounddevice soundfile numpy pydub claudette
```

After installing pynvim, make sure to set up Python for Neovim before installing VoiceTex. Add one of the following to your Neovim configuration:

For Vim script:
```vim
let g:python3_host_prog = '/path/to/python3'
```

For Lua:
```lua
vim.g.python3_host_prog = '/path/to/python3'
```

Replace '/path/to/python3' with the actual path to your Python 3 executable.

### API Keys

Set up your API keys as global environment variables:

```bash
export OPENAI_API_KEY='your_openai_api_key'
export ANTHROPIC_API_KEY='your_anthropic_api_key'
```

### Installing with Packer

Add the following to your Neovim configuration:

```lua
use {
  'wazizian/voicetex.nvim',
  run = ':UpdateRemotePlugins',
  config = function()
    require('voicetex').setup()
  end
}
```

After installation, restart Neovim for the changes to take effect.

## Configuration

You can customize the stop key for recording (default is Enter):

```lua
require('voicetex').setup({
  stop_key = '<C-c>'  -- Use Ctrl+C to stop recording
})
```

## Usage

1. Start recording:
   ```
   :VoiceTexRecord
   ```
   Dictate your LaTeX content and press the configured stop key (default: Enter) to finish.
    
   The plugin will transcribe your audio, convert it to LaTeX, and insert it at the cursor position, taking into account the local document context.

2. Optionally, add context files to improve LaTeX conversion accuracy:
   ```
   :VoiceTexContext file1.tex file2.tex
   ```
   This command uses Anthropic's prompt caching to reduce API costs.

VoiceTex is designed for professional use in academic and scientific writing, offering a powerful tool for hands-free LaTeX document creation. It uses OpenAI's Whisper model for audio transcription and Anthropic's Claude model for LaTeX conversion, while leveraging local context to improve LaTeX formatting accuracy.

## TODO

- Implement lazy loading to improve startup time and resource usage

## Development

Clone this repo.

Following `pynvim` recommendations, create `dummy_vimrc` at root containing
```
let &runtimepath.=','.escape(expand('<sfile>:p:h'), '\,')
```
Now launch `neovim` with
```
nvim -u ./dummy_vimrc
```
and run 
```
:UpdateRemotePlugins
:lua require("voicetex").setup()
```
This `neovim` instance will then be using the local version of this plugin.
