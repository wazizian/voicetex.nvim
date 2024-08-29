from recorder import Recorder
from transcriber import Transcriber

if __name__ == "__main__":
    recorder = Recorder()
    recorder.record()
    recorder.playback()

    transcriber = Transcriber()
    transcription = transcriber.transcribe(recorder.last_recording)
    print("Transcription:", transcription)
