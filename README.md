# VoiceTex

VoiceTex is a Neovim plugin that allows you to dictate LaTeX content using your voice. It transcribes your speech and converts it into properly formatted LaTeX code, making it easier to write mathematical documents hands-free.

## Goal

The main goal of VoiceTex is to provide a seamless voice-to-LaTeX experience within Neovim. It aims to:

1. Record audio input from the user
2. Transcribe the audio to text
3. Convert the transcribed text into valid LaTeX code
4. Insert the resulting LaTeX code at the cursor position in Neovim

This plugin is particularly useful for mathematicians, scientists, or anyone who frequently works with LaTeX and wants to speed up their document creation process or reduce strain from typing.

## Installation

### Dependencies

Before installing VoiceTex, ensure you have the following dependencies:

- Neovim (0.5.0 or later)
- Python 3.6 or later
- OpenAI API key (for transcription)
- Anthropic API key (for LaTeX conversion)

You also need to install the following Python packages:

```bash
pip install pynvim openai sounddevice soundfile numpy pydub claudette
```

### Installing with Packer

To install VoiceTex using Packer, add the following to your Neovim configuration:

```lua
use {
  'path/to/voicetex',
  run = ':UpdateRemotePlugins',
  config = function()
    require('voicetex').setup()
  end
}
```

Replace `'path/to/voicetex'` with the actual path or GitHub repository URL of the VoiceTex plugin.

### Configuration

After installation, you need to set up your API keys. Add the following to your Neovim configuration or shell environment:

```lua
vim.env.OPENAI_API_KEY = 'your_openai_api_key'
vim.env.ANTHROPIC_API_KEY = 'your_anthropic_api_key'
```

You can customize the stop key for recording by passing it to the setup function:

```lua
require('voicetex').setup({
  stop_key = '<C-c>'  -- Use Ctrl+C to stop recording
})
```

## Usage

1. Start a new recording:
   ```
   :VoiceTexRecord
   ```
   Speak your LaTeX content. Press the configured stop key (default is Enter) to stop recording.

2. Add context files:
   ```
   :VoiceTexContext file1.tex file2.tex
   ```
   This helps improve the accuracy of LaTeX conversion by providing existing document context.

3. The transcribed and converted LaTeX code will be inserted at your cursor position.

Remember to be in a LaTeX file or environment for the best results.

Enjoy using VoiceTex to create your LaTeX documents with voice input!
