from langchain.tools import tool
from tool.audio_tool import AudioAgent

# Wrapper for AudioAgent to expose as a LangChain tool

audio_agent = AudioAgent()

generate_audio_from_text = audio_agent.generate_audio_from_text

generate_text_from_audio = audio_agent.generate_text_from_audio
