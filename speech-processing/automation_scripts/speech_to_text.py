#!pip install gTTS

from gtts import gTTS
from pathlib import Path

# Text you want to convert to audio
text = "Hello, and welcome to this recording. In today’s session, we’re exploring the importance of clear communication. Whether in personal relationships, professional settings, or even day-to-day interactions, effective communication is key. It allows us to express our thoughts, share information, and build stronger connections with those around us. One important aspect of communication is active listening, where we focus not only on what is being said but also on the intent and emotion behind the words. By being attentive and showing empathy, we create a more supportive environment for open and honest conversations. Thank you for listening."

# Set language (e.g., 'en' for English)
language = 'en'

# Create a gTTS object
tts = gTTS(text=text, lang=language, slow=False)

# Get the current directory
current_directory = Path.cwd()

# Get the parent directory (one level up)
parent_directory = current_directory.parent

# Save the audio file
tts.save(f"{parent_directory}/test_files/{language}_audio.wav")

print(f"Audio file has been saved as {language}_audio.wav")