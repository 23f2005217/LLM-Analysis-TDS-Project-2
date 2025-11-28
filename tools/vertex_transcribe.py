from langchain_core.tools import tool
from google import genai
from google.genai import types
import os

@tool
def transcribe_audio(file_path: str) -> str:
    """
    Transcribe an audio file using Google's Gemini model.
    
    Args:
        file_path (str): Local path to the audio file.
        
    Returns:
        str: Transcription text.
    """
    api_key = os.getenv("VERTEX_API_KEY")
    if not api_key:
        return "Error: VERTEX_API_KEY not set."
        
    client = genai.Client(api_key=api_key)
    
    try:
        if not os.path.exists(file_path):
            return f"Error: File {file_path} not found."

        with open(file_path, "rb") as f:
            audio_bytes = f.read()
            
        ext = os.path.splitext(file_path)[1].lower()
        mime_type = "audio/mp3"
        if ext == ".wav": mime_type = "audio/wav"
        elif ext == ".m4a": mime_type = "audio/m4a"
        elif ext == ".ogg": mime_type = "audio/ogg"
        elif ext == ".mp4": mime_type = "audio/mp4"
        elif ext == ".mpeg": mime_type = "audio/mpeg"
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[
                types.Content(
                    parts=[
                        types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
                        types.Part.from_text(text="Transcribe this audio exactly.")
                    ]
                )
            ]
        )
        return response.text
    except Exception as e:
        return f"Error transcribing audio: {e}"