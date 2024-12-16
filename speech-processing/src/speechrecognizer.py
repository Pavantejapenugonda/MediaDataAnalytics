import whisper
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SpeechRecognizer:
    def __init__(self, model_path):
        """
        Initializes the SpeechRecognizer with a specified Whisper model and device.

        Args:
            model_path (str): Path to the Whisper model.
            device (str, optional): Device to load the model on ('cpu' or 'cuda'). 
                                    If None, defaults to GPU if available, otherwise CPU.
        """
        try:
            self.model = whisper.load_model(model_path)
            logging.info(f"Whisper model loaded")
        except Exception as e:
            logging.error("Failed to load Whisper model", exc_info=True)
            self.model = None  # Set model to None to indicate failure

    def load_audio(self, audio_path):
        """
        Loads an audio file and moves it to the specified device.

        Args:
            audio_path (str): Path to the audio file.

        Returns:
            torch.Tensor or None: Loaded audio data on the specified device, or None if failed.
        """
        if self.model is None:
            logging.error("Model is not loaded, cannot load audio.")
            return None
        
        try:
            audio = whisper.load_audio(audio_path)
            logging.info(f"Audio loaded from {audio_path}")
            return audio
        except Exception as e:
            logging.error(f"Error loading audio from {audio_path}", exc_info=True)
            return None
    
    def detect_language(self, audio):
        """
        Detects the language of the given audio data.

        Args:
            audio (torch.Tensor): Audio data tensor.

        Returns:
            tuple: Detected language code and success status.
        """
        if audio is None:
            return None, False
        
        try:
            audio = whisper.pad_or_trim(audio)
            mel = whisper.log_mel_spectrogram(audio)
            _, probs = self.model.detect_language(mel)
            detected_language = max(probs, key=probs.get)
            logging.info(f"Detected language: {detected_language}")
            return detected_language, True
        except Exception as e:
            logging.error("Error detecting language", exc_info=True)
            return None, False
    
    def decode_audio(self, audio):
        """
        Decodes the audio data to text.

        Args:
            audio (torch.Tensor): Audio data tensor.

        Returns:
            tuple: Decoded text and success status.
        """
        if audio is None:
            return None, False
        
        try:
            audio = whisper.pad_or_trim(audio)
            mel = whisper.log_mel_spectrogram(audio)
            options = whisper.DecodingOptions()
            result = whisper.decode(self.model, mel, options)
            logging.info("Audio decoding completed successfully")
            return result.text, True
        except Exception as e:
            logging.error("Error decoding audio", exc_info=True)
            return None, False
