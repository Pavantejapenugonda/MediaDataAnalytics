import whisper
vi_audio = r"C:\Users\ppenugonda\Downloads\test_speech_to_text\vi_audio.wav"
en_audio = "C:/Users/ppenugonda/Downloads/en_audio.wav"
sp_audio = r"C:\Users\ppenugonda\OneDrive - SS8 Networks Inc\Documents\speech-processing\test_data\spanish_audio.mp3"
ar_audio= r"C:\Users\ppenugonda\OneDrive - SS8 Networks Inc\Documents\speech-processing\test_data\arabic_audio.m4a"
en_sp_audio = r"C:\Users\ppenugonda\OneDrive - SS8 Networks Inc\Documents\speech-processing\test_data\eng_spanish_audio.m4a"

model = whisper.load_model("tiny")
audio = whisper.load_audio(sp_audio)
audio = whisper.pad_or_trim(audio)
mel = whisper.log_mel_spectrogram(audio)
_, probs = model.detect_language(mel)
print(probs)
detected_language = max(probs, key=probs.get)
print(detected_language)

transcribe_data = model.transcribe(audio, task="transcribe")
print(transcribe_data)