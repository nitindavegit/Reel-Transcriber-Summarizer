import os
import uuid
import requests
import whisper

model = whisper.load_model("large-v3")

def download_audio(audio_url: str) -> str:
    filename = f"temp_{uuid.uuid4().hex}.mp4"
    
    r = requests.get(audio_url, stream=True)
    
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=4096):
            f.write(chunk)
    return filename

def transcribe_audio(audio_url: str) -> str:
    file = download_audio(audio_url)    # local path to downloaded mp4 

    result = model.transcribe(file) # proper dictionary with keys: "text", "segments", "words"

    transcript = result["text"].strip() # full spoken words text from the reel
    
    os.remove(file) # remove the file after transcribing
    return transcript
