from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import time
import logging
from src.speechrecognizer import SpeechRecognizer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Define a Pydantic model for audio data
class AudioData(BaseModel):
    audio_file: str
    translate_lang_code: str | None = None

# Create an instance of SpeechRecognizer
recognizer = SpeechRecognizer("large-v2")
models_mapping = {'en': SpeechRecognizer("tiny")}

# Custom exception handler for ValueError
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    logging.error("ValueError encountered", exc_info=True)
    return JSONResponse(
        status_code=400,
        content={"error": {"code": 400, "type": "Validation Error", "message": str(exc)}}
    )

# Health check endpoint
@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Health check endpoint to verify the service's status.

    Returns:
        JSONResponse: {"status": "healthy"} if service is running correctly.
                      {"status": "unhealthy", "details": error details} if not.
    """
    try:
        logging.info("Health check request received")
        return JSONResponse(status_code=200, content={"status": "healthy"})
    except Exception as e:
        logging.error("Health check failed", exc_info=True)
        return JSONResponse(
            status_code=503,
            content={"error": {"code": 503, "type": "Service Unavailable", "message": str(e)}}
        )

# Endpoint for detecting language
@app.post("/detect-language/", tags=["Language Detection"])
async def detect_language(audio_file: AudioData):
    """
    Detects the language of the provided audio file.

    Args:
        audio_file (AudioData): Pydantic model with the path to the audio file.

    Returns:
        dict: Detected language code.

    Raises:
        HTTPException: If there is an error during language detection.
    """
    try:
        logging.info(f"Language detection request received for file: {audio_file.audio_file}")
        audio = recognizer.load_audio(audio_file.audio_file)
        detected_language = recognizer.detect_language(audio)
        logging.info(f"Detected language: {detected_language}")
        return {"detect-language_text": detected_language}
    except FileNotFoundError:
        logging.error("Audio file not found", exc_info=True)
        raise HTTPException(status_code=404, detail="Audio file not found.")
    except ValueError as ve:
        logging.error("Invalid value provided", exc_info=True)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error("Unexpected error in language detection", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": {"code": 500, "type": "Server Error", "message": "An unexpected error occurred."}}
        )

# Endpoint for transcribing audio
@app.post("/transcribe/", tags=["Transcription"])
async def decode_basic_audio(audio_file: AudioData):
    """
    Transcribes the provided audio file to text.

    Args:
        audio_file (AudioData): Pydantic model with the path to the audio file.

    Returns:
        dict: Transcription result with text and metadata.

    Raises:
        HTTPException: If there is an error during transcription.
    """
    try:
        elasped_lang_time = 0
        logging.info(f"Transcription request received for file: {audio_file.audio_file}")
        start_time = time.time()
        audio = recognizer.load_audio(audio_file.audio_file)
        if audio is None:
            return JSONResponse(status_code=400, content={"detail": "Failed to load audio."})
        
        # Use the provided translation language code directly
        translate_lang_code = audio_file.translate_lang_code
        if translate_lang_code:
            # Check if the language code is valid based on your models mapping
            if translate_lang_code in models_mapping:
                result = models_mapping[translate_lang_code].model.transcribe(audio, language=translate_lang_code, task="transcribe")
            else:
                return JSONResponse(status_code=400, content={"detail": f"Language code '{translate_lang_code}' is not supported."})
        else:
            lang_start_time = time.time()
            # If no language code is provided, fall back to detected language
            detected_language, success = recognizer.detect_language(audio)
            elasped_lang_time = time.time() - lang_start_time
            logging.info(f"Time taken for langiuage detection in {elasped_lang_time:.2f} seconds and detected lang : {detected_language}")
            if not success:
                return JSONResponse(status_code=400, content={"detail": "Failed to detect language."})
            if detected_language in models_mapping:
                result = models_mapping[detected_language].model.transcribe(audio, language=translate_lang_code, task="transcribe")
            else:
                result = recognizer.model.transcribe(audio, language=detected_language, task="transcribe")

        elapsed_time = time.time() - start_time
        logging.info(f"Transcription completed in {elapsed_time:.2f} seconds")
        return {
            "transcribe_text": result['text'],
            "metadata": {
                "time_taken": {"lang_detection" : elasped_lang_time, "total_time_taken":elapsed_time},
                "filepath": audio_file.audio_file
            }
        }
    except FileNotFoundError:
        logging.error("Audio file not found", exc_info=True)
        raise HTTPException(status_code=404, detail="Audio file not found.")
    except ValueError as ve:
        logging.error("Invalid value provided", exc_info=True)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error("Unexpected error in transcription", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": {"code": 500, "type": "Server Error", "message": "An unexpected error occurred."}}
        )

# Endpoint for translating audio
@app.post("/translate/", tags=["Translation"])
async def translate_audio(audio_file: AudioData):
    """
    Translates the provided audio file to the specified language.

    Args:
        audio_file (AudioData): Pydantic model with the path to the audio file and optional target language code.

    Returns:
        dict: Translated text from the audio.

    Raises:
        HTTPException: If there is an error during translation.
    """
    try:
        logging.info(f"Translation request received for file: {audio_file.audio_file} to {audio_file.translate_lang_code}")
        
        if not audio_file.translate_lang_code:
            raise HTTPException(status_code=400, detail="No translation language code provided.")
        
        # Directly use the provided translate_lang_code for transcription
        result = recognizer.model.transcribe(audio_file.audio_file, language=audio_file.translate_lang_code, task="transcribe")
        logging.info("Translation completed successfully")
        return {"translate_text": result['text']}
    except FileNotFoundError:
        logging.error("Audio file not found", exc_info=True)
        raise HTTPException(status_code=404, detail="Audio file not found.")
    except ValueError as ve:
        logging.error("Invalid value provided", exc_info=True)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error("Unexpected error in translation", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": {"code": 500, "type": "Server Error", "message": "An unexpected error occurred."}}
        )
