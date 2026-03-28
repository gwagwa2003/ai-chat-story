#from openai import OpenAI
import openai
from config import get_openai_api_key

# Initialize the OpenAI client

# Open the audio file
def stt(filepath):
  openai.api_key = get_openai_api_key()
  with open(filepath, "rb") as audio_file:
    # Create the transcription
    transcript = openai.audio.transcriptions.create(
      model="whisper-1",
      file=audio_file,
      response_format="verbose_json",
      language="zh"
    )

  print(transcript.text)
  return transcript.text


