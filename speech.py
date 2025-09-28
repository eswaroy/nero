import speech_recognition as sr
import pyttsx3
import logging
import threading
import queue
from config import Config

logger = logging.getLogger(__name__)

class SpeechManager:
    def __init__(self):
        self.config = Config()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize TTS engine
        self.engine = pyttsx3.init()
        self._configure_tts()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Speech queue for thread-safe TTS
        self.speech_queue = queue.Queue()
        self.tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
        self.tts_thread.start()
        
        logger.info("Speech manager initialized")
    
    def _configure_tts(self):
        """Configure text-to-speech settings"""
        voices = self.engine.getProperty('voices')
        if voices:
            voice_index = min(self.config.get("voice_index"), len(voices) - 1)
            self.engine.setProperty('voice', voices[voice_index].id)
        
        self.engine.setProperty('rate', self.config.get("speech_rate"))
        self.engine.setProperty('volume', self.config.get("volume"))
    
    def speak(self, text, interrupt=False):
        """Add text to speech queue"""
        if interrupt:
            # Clear queue for urgent messages
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                except queue.Empty:
                    break
        
        self.speech_queue.put(text)
    
    def _tts_worker(self):
        """Background worker for text-to-speech"""
        while True:
            try:
                text = self.speech_queue.get()
                if text:
                    self.engine.say(text)
                    self.engine.runAndWait()
                self.speech_queue.task_done()
            except Exception as e:
                logger.error(f"TTS error: {e}")
    
    def listen(self, timeout=10, phrase_time_limit=8):
        """Listen for user speech with improved error handling"""
        try:
            with self.microphone as source:
                logger.info("Listening for user input...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            # Recognize speech
            command = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized: {command}")
            return command.lower()
            
        except sr.WaitTimeoutError:
            logger.warning("Listening timeout")
            return None
        except sr.UnknownValueError:
            logger.warning("Speech not understood")
            self.speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            self.speak("Sorry, my speech service is temporarily unavailable.")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in speech recognition: {e}")
            return None
    
    def get_voices(self):
        """Get available voices"""
        return self.engine.getProperty('voices')
    
    def set_voice(self, index):
        """Set voice by index"""
        voices = self.get_voices()
        if 0 <= index < len(voices):
            self.engine.setProperty('voice', voices[index].id)
            self.config.set("voice_index", index)
            return True
        return False
