import queue
import sounddevice as sd
import vosk
import json
import wave
import whisper
from kokoro import KPipeline
#
import warnings
# Suppress specific categories
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# ----------------------------
# Settings
# ----------------------------
MODEL_PATH = "vosk-model-en-us-0.42-gigaspeech" #"vosk-model-small-en-us-0.15"  # Path to vosk model folder (downloaded + unzipped)
WAKE_WORD = "okay amy"
OUTPUT_FILENAME = "Recorded.wav"
RECORD_SECONDS = 8
RATE = 16000
CHANNELS = 1
CHUNK = 1024

# ----------------------------
# Wake word listener
# ----------------------------
model = vosk.Model(MODEL_PATH)
repo_id='hexgrad/Kokoro-82M'
pipeline = KPipeline(lang_code='a', repo_id=repo_id)
q = queue.Queue()

def audio_callback(indata, frames, time, status):
    """Collect microphone input in queue for Vosk processing"""
    if status:
        print(status)
    q.put(bytes(indata))

def listen_for_wake_word():
    """Continuously listens until the wake word is detected"""
    recognizer = vosk.KaldiRecognizer(model, RATE)

    with sd.RawInputStream(samplerate=RATE, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
        print("Listening for wake word... Say 'okay amy'")

        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower()
                if text:
                    print("Heard:", text)
                if WAKE_WORD in text:
                    print("Wake word detected!")
                    speak("I am up.")
                    return True

# ----------------------------
# Recording function
# ----------------------------
def record_audio(output_filename=OUTPUT_FILENAME, record_seconds=RECORD_SECONDS):
    """Record audio for N seconds and save to WAV"""
    print(f"Recording for {record_seconds} seconds...")

    p = sd.RawInputStream(samplerate=RATE, blocksize=CHUNK, dtype='int16',
                          channels=CHANNELS)
    frames = []

    with p:
        for _ in range(0, int(RATE / CHUNK * record_seconds)):
            frames.append(p.read(CHUNK)[0])

    # Save WAV file
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)  # 16-bit PCM = 2 bytes
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    #print(f"Saved recording to {output_filename}")

#transcribe the audios
def transcribe_audio(filename, model_name="small"):
    print("Transcribing...")
    speak("Processing your request.")
    model = whisper.load_model(model_name)
    result = model.transcribe(filename)
    return result["text"]

#speak converted audio to text
def speak(text):
    generator = pipeline(text, voice='af_heart')

    # Play and save each chunk
    for i, (gs, ps, audio) in enumerate(generator):
        #print(f"Chunk {i}: Graphemes: {gs}, Phonemes: {ps}")
        
        # Play audio chunk
        sd.play(audio, samplerate=24000)
        sd.wait()  # Wait until this chunk finishes playings
# ----------------------------
# Main
# ----------------------------
# if __name__ == "__main__":
#     while True:
#         if listen_for_wake_word():   # Wait for "Ok Amy"
#             record_audio()           # Record 5 seconds
#             print("You can now transcribe or process the audio...")
#             text = transcribe_audio(OUTPUT_FILENAME)
#             print("Transcription:", text)
#             speak(text)