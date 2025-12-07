from scraper.insta_fetcher import get_audio_url
from transcriber.whisper_runner import transcribe_audio
from summarizer.llm_summary import summarize

async def process_reel(url: str) -> dict:
    audio_url = await get_audio_url(url) # Video URL of the reel
    transcript = transcribe_audio(audio_url)    # Full spoken words text from the reel
    summary_data = summarize(transcript)         # A Python dict containing: "summary" and "lessons"

    
    return {
        "transcript": transcript,
        "summary": summary_data.get("summary", ""),
        "lessons": summary_data.get("lessons", "")
    }
