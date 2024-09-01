# VoiceTex

VoiceTex is a Neovim plugin that enables voice-to-LaTeX functionality, allowing users to dictate mathematical content directly into their documents. It provides a seamless integration of speech recognition and LaTeX formatting within the Neovim environment.

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
  'path/to/voicetex',
  run = ':UpdateRemotePlugins',
  config = function()
    require('voicetex').setup()
  end
}
```

Replace `'path/to/voicetex'` with the actual path or GitHub repository URL of the VoiceTex plugin.

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

2. Add context files to improve LaTeX conversion accuracy:
   ```
   :VoiceTexContext file1.tex file2.tex
   ```
   This command uses Anthropic's prompt caching to reduce API costs.

3. The plugin will transcribe your audio, convert it to LaTeX, and insert it at the cursor position, taking into account the local document context.

VoiceTex is designed for professional use in academic and scientific writing, offering a powerful tool for hands-free LaTeX document creation. It uses OpenAI's Whisper model for audio transcription and Anthropic's Claude model for LaTeX conversion, while leveraging local context to improve LaTeX formatting accuracy.
