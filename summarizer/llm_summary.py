import subprocess
import logging

OLLAMA_MODEL = "phi3:mini"

PROMPT = """
You are an expert summarizer of Instagram reels.

Given the transcript below, do two things:
1. Write a bullet-point SUMMARY of what is said.
2. Write key LESSONS / PSYCHOLOGY INSIGHTS if any.

Format your reply EXACTLY like this:

SUMMARY:
- point 1
- point 2
- point 3

LESSONS:
- lesson 1
- lesson 2
(or write "None" if there are no lessons)

Transcript:
{transcript}
"""

def summarize(transcript: str) -> dict:
    # Build prompt
    prompt = PROMPT.format(transcript=transcript)

    # Call local LLM via Ollama
    result = subprocess.run(
    ["ollama", "run", OLLAMA_MODEL],
    input=prompt,
    text=True,
    capture_output=True,
    encoding="utf-8",           
    errors="ignore"            
)

    output = result.stdout.strip() # contains only the raw output from the LLM


    # Debug, log first part of raw output
    logging.info("LLM raw output (first 300 chars): %s", output[:300].replace("\n", "\\n"))

    # Default values
    summary_text = ""
    lessons_text = ""

    # Parse by markers instead of JSON
    if "SUMMARY:" in output:
        # Split at SUMMARY
        before_summary, after_summary = output.split("SUMMARY:", 1)

        # Now check if LESSONS exists
        if "LESSONS:" in after_summary:
            summary_part, lessons_part = after_summary.split("LESSONS:", 1)
        else:
            summary_part, lessons_part = after_summary, ""

        summary_text = summary_part.strip()
        lessons_text = lessons_part.strip()
    else:
        # Fallback: treat full output as summary
        summary_text = output.strip()
        lessons_text = ""

    return {
        "summary": summary_text,
        "lessons": lessons_text
    }
