import argparse
from recorder import Recorder
from transcriber import Transcriber
from postprocessor import ClaudePostProcessor

def main():
    parser = argparse.ArgumentParser(description="Record, transcribe, and postprocess audio.")
    parser.add_argument('--context', nargs='+', help='Paths to context files')
    parser.add_argument('--provider', choices=['claude'], default='claude', help='Choose the postprocessing provider (default: claude)')
    args = parser.parse_args()

    recorder = Recorder()
    recorder.record()

    transcriber = Transcriber()
    transcription = transcriber.transcribe(recorder.last_recording)

    postprocessor = ClaudePostProcessor()
    if args.context:
        postprocessor.add_context_from_files(*args.context)
    final_transcription = postprocessor.postprocess_transcription(transcription)
    print("Original Transcription:", transcription)
    print("Postprocessed Transcription:", final_transcription)

if __name__ == "__main__":
    main()
