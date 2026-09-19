import sounddevice as sd
import soundfile as sf
import tempfile
import os
import openai
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

SAMPLE_RATE = 160000  # Sample rate for recording
MAX_DURATION = 30  # Maximum duration of recording in seconds
SAMPLES = SAMPLE_RATE * MAX_DURATION  # Total number of samples to record

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Initialize OpenAI client with API key

def record_audio():
    input("Press Enter to start recording your voice")
    print("Recording... Press Enter to stop.")

    audio_data = sd.rec(int(SAMPLES), samplerate=SAMPLE_RATE, channels=1, dtype='float64')
    input()  # Wait for user to press Enter to stop recording
    sd.stop()  # Stop recording
    print("Recording stopped.")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(tmp.name, audio_data, SAMPLE_RATE)  # Save the recorded audio to a file
    print(f"Audio saved {tmp.name}")


def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        output = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    return output.text  # Return the transcribed text from the audio file


record_audio()


