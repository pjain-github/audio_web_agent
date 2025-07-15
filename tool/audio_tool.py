from langchain.tools import tool
from typing import Optional
import tempfile
import asyncio
import edge_tts
import whisper


class AudioAgent:
    def __init__(self):
        pass

    @tool("generate_audio_from_text", return_direct=True)
    def generate_audio_from_text(
        self,
        text: str,
        rate: Optional[str] = "-2%",
        pitch: Optional[str] = "-1Hz"
    ) -> str:
        """
        Generate audio from text using Edge TTS.
        Args:
            text: The text to convert to speech.
            rate: Speaking rate for edge_tts.
            pitch: Pitch for edge_tts.
        Returns:
            Path to the generated audio file.
        """
        return asyncio.run(self._edge_tts(text, rate, pitch))

    async def _edge_tts(self, text, rate, pitch):
        voice = "en-US-ChristopherNeural"
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tts = edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch)
        await tts.save(temp_file.name)
        return temp_file.name

    @tool("generate_text_from_audio", return_direct=True)
    def generate_text_from_audio(
        self,
        audio_file: str
    ) -> str:
        """
        Generate text from audio using Whisper ASR.
        Args:
            audio_file: Path to the audio file.
        Returns:
            Transcribed text as a string.
        """
        model = whisper.load_model("tiny")
        result = model.transcribe(audio_file)
        return result["text"].strip()