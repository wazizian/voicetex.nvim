from recorder import Recorder
from transcriber import Transcriber
from postprocessor import GPTPostProcessor

if __name__ == "__main__":
    recorder = Recorder()
    recorder.record()

    transcriber = Transcriber()
    transcription = transcriber.transcribe(recorder.last_recording)

    postprocessor = GPTPostProcessor()
    final_transcription = postprocessor.postprocess_transcription(transcription)
    print("Transcription:", transcription)
