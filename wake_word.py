import openwakeword
import openwakeword.model
import numpy as np
import pyaudio
import threading
import logging
import time
from config import Config

logger = logging.getLogger(__name__)

class OpenWakeWordDetector:
    def __init__(self):
        self.config = Config()
        self.model = None
        self.audio = None
        self.stream = None
        self.is_listening = False
        self.detection_thread = None
        self.callback = None
        
        # Audio configuration
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 1024
        
    def initialize(self, callback):
        """Initialize the wake word detector with custom model"""
        try:
            model_path = self.config.get("wake_word_model_path")
            
            # Try to load custom model first, fallback to built-in models
            try:
                if model_path and model_path.endswith('.tflite'):
                    self.model = openwakeword.model.Model(
                        wakeword_models=[model_path],
                        inference_framework='tflite'
                    )
                    logger.info(f"Loaded custom wake word model: {model_path}")
                else:
                    # Fallback to pre-trained models
                    self.model = openwakeword.model.Model(
                        wakeword_models=["hey_jarvis_v0.1"]
                    )
                    logger.info("Using built-in wake word model: hey_jarvis")
                    
            except Exception as e:
                logger.warning(f"Custom model failed, using built-in: {e}")
                self.model = openwakeword.model.Model(
                    wakeword_models=["hey_jarvis_v0.1"]
                )
            
            self.callback = callback
            self._initialize_audio()
            return True
            
        except Exception as e:
            logger.error(f"Wake word initialization failed: {e}")
            return False
    
    def _initialize_audio(self):
        """Initialize audio stream"""
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        logger.info("Audio stream initialized")
    
    def start_listening(self):
        """Start listening for wake word in separate thread"""
        if self.is_listening:
            return
            
        self.is_listening = True
        self.detection_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.detection_thread.start()
        logger.info("Wake word detection started")
    
    def stop_listening(self):
        """Stop wake word detection"""
        self.is_listening = False
        if self.detection_thread:
            self.detection_thread.join(timeout=1.0)
        logger.info("Wake word detection stopped")
    
    def _listen_loop(self):
        """Main listening loop"""
        threshold = self.config.get("wake_word_threshold")
        
        while self.is_listening:
            try:
                # Read audio data
                audio_data = np.frombuffer(
                    self.stream.read(self.chunk, exception_on_overflow=False),
                    dtype=np.int16
                )
                
                # Get predictions
                predictions = self.model.predict(audio_data)
                
                # Check for wake word detection
                for wake_word in predictions:
                    confidence = predictions[wake_word]
                    if confidence > threshold:
                        logger.info(f"Wake word detected: {wake_word} (confidence: {confidence:.2f})")
                        if self.callback:
                            threading.Thread(target=self.callback, daemon=True).start()
                        time.sleep(2)  # Prevent multiple detections
                        break
                        
            except Exception as e:
                logger.error(f"Error in wake word detection: {e}")
                time.sleep(0.1)
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_listening()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()
        logger.info("Wake word detector cleaned up")
