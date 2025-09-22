# import sys
# import logging
# import threading
# import time
# import signal
# import os
# import asyncio
# from pathlib import Path

# # Add current directory to path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# # Import optimized modules
# from config import Config
# from speech import SpeechManager
# from commands import CommandExecutor
# from model import IntentClassifier
# from database import DatabaseManager
# from gui import ModernVoiceAssistantGUI

# # Configure comprehensive logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('eight_assistant.log'),
#         logging.StreamHandler(sys.stdout)
#     ]
# )
# # Enhanced logging configuration with Windows Unicode support
# def setup_logging():
#     """Setup logging with Windows Unicode support"""
#     try:
#         # Try to set UTF-8 encoding for Windows console
#         import sys
#         if sys.platform.startswith('win'):
#             import os
#             os.system('chcp 65001 >nul 2>&1')  # Set console to UTF-8
#     except:
#         pass
    
#     # Create custom formatter without emojis for file logging
#     class SafeFormatter(logging.Formatter):
#         def format(self, record):
#             # Remove emojis from log messages for file output
#             message = super().format(record)
#             # Replace common emojis with text equivalents
#             emoji_replacements = {
#                 '🚀': '[ROCKET]',
#                 '🎙️': '[MIC]',
#                 '🐍': '[PYTHON]',
#                 '📁': '[FOLDER]',
#                 '✅': '[SUCCESS]',
#                 '⚠️': '[WARNING]',
#                 '🧠': '[BRAIN]',
#                 '🔑': '[KEY]',
#                 '🎨': '[ART]',
#                 '🎯': '[TARGET]',
#                 '💻': '[COMPUTER]',
#                 '🔧': '[TOOL]',
#                 '📄': '[DOCUMENT]',
#                 '⚙️': '[SETTINGS]',
#                 '🌐': '[WEB]',
#                 '⏰': '[TIME]',
#                 '📅': '[CALENDAR]',
#                 '🔊': '[VOLUME_UP]',
#                 '🔉': '[VOLUME_DOWN]',
#                 '🔇': '[MUTE]',
#                 '📸': '[CAMERA]',
#                 '⌨️': '[KEYBOARD]',
#                 '🏪': '[STORE]',
#                 '📚': '[BOOKS]',
#                 '🌤️': '[WEATHER]',
#                 '🌡️': '[TEMPERATURE]',
#                 '💧': '[WATER]',
#                 '💨': '[WIND]',
#                 '❌': '[ERROR]',
#                 '❓': '[QUESTION]',
#                 '💬': '[CHAT]',
#                 '🎙️': '[LIVE]',
#                 '🛑': '[STOP]',
#                 '👤': '[USER]',
#                 '🤖': '[BOT]',
#                 '📊': '[STATS]',
#                 '🔍': '[SEARCH]',
#                 '📰': '[NEWS]',
#                 '💡': '[IDEA]',
#                 '🧹': '[CLEAN]',
#                 '👋': '[WAVE]',
#                 '💥': '[CRASH]',
#                 '📋': '[CLIPBOARD]'
#             }
            
#             for emoji, replacement in emoji_replacements.items():
#                 message = message.replace(emoji, replacement)
            
#             return message
    
#     # Console handler with emoji support
#     console_handler = logging.StreamHandler(sys.stdout)
#     console_handler.setLevel(logging.INFO)
    
#     # File handler with safe formatter
#     file_handler = logging.FileHandler('eight_assistant.log', encoding='utf-8')
#     file_handler.setLevel(logging.DEBUG)
#     file_handler.setFormatter(SafeFormatter(
#         '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     ))
    
#     # Configure root logger
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#         handlers=[console_handler, file_handler]
#     )

# # Call setup_logging before any other imports
# setup_logging()

# logger = logging.getLogger(__name__)

# class OpenWakeWordDetector:
#     """Enhanced wake word detector using OpenWakeWord"""
#     def __init__(self):
#         self.config = Config()
#         self.model = None
#         self.audio = None
#         self.stream = None
#         self.is_listening = False
#         self.detection_thread = None
#         self.callback = None
        
#         # Audio configuration
#         self.audio_format = None
#         self.channels = 1
#         self.rate = 16000
#         self.chunk = 1024
        
#         try:
#             import pyaudio
#             self.audio_format = pyaudio.paInt16
#         except ImportError:
#             logger.error("PyAudio not installed. Audio functionality limited.")
    
#     def initialize(self, callback):
#         """Initialize the wake word detector"""
#         try:
#             # Try to import OpenWakeWord
#             try:
#                 import openwakeword
#                 import openwakeword.model
#                 import numpy as np
#                 import pyaudio
                
#                 self.np = np
#                 self.pyaudio = pyaudio
                
#                 model_path = self.config.get("wake_word_model_path")
                
#                 # Try custom model first, fallback to built-in
#                 try:
#                     if model_path and Path(model_path).exists():
#                         self.model = openwakeword.model.Model(
#                             wakeword_models=[model_path],
#                             inference_framework='tflite'
#                         )
#                         logger.info(f"Loaded custom wake word model: {model_path}")
#                     else:
#                         # Use built-in model
#                         self.model = openwakeword.model.Model(
#                             wakeword_models=["hey_jarvis_v0.1"]
#                         )
#                         logger.info("Using built-in wake word model: hey_jarvis")
                        
#                 except Exception as e:
#                     logger.warning(f"OpenWakeWord model failed, using volume detection: {e}")
#                     return self._initialize_fallback_detector(callback)
                
#                 self.callback = callback
#                 self._initialize_audio()
#                 return True
                
#             except ImportError:
#                 logger.warning("OpenWakeWord not available, using fallback detection")
#                 return self._initialize_fallback_detector(callback)
                
#         except Exception as e:
#             logger.error(f"Wake word initialization failed: {e}")
#             return self._initialize_fallback_detector(callback)
    
#     def _initialize_fallback_detector(self, callback):
#         """Initialize simple volume-based fallback detector"""
#         try:
#             import pyaudio
            
#             self.callback = callback
#             self.is_fallback = True
#             self._initialize_audio()
#             logger.info("Fallback volume detector initialized")
#             return True
            
#         except Exception as e:
#             logger.error(f"Fallback detector failed: {e}")
#             return False
    
#     def _initialize_audio(self):
#         """Initialize audio stream with compatibility"""
#         try:
#             import pyaudio
            
#             self.audio = pyaudio.PyAudio()
            
#             # Try with exception_on_overflow parameter first (newer PyAudio)
#             try:
#                 self.stream = self.audio.open(
#                     format=self.audio_format,
#                     channels=self.channels,
#                     rate=self.rate,
#                     input=True,
#                     frames_per_buffer=self.chunk,
#                     exception_on_overflow=False
#                 )
#             except TypeError:
#                 # Fallback for older PyAudio versions
#                 logger.info("Using PyAudio compatibility mode (no exception_on_overflow)")
#                 self.stream = self.audio.open(
#                     format=self.audio_format,
#                     channels=self.channels,
#                     rate=self.rate,
#                     input=True,
#                     frames_per_buffer=self.chunk
#                 )
            
#             logger.info("Audio stream initialized successfully")
            
#         except Exception as e:
#             logger.error(f"Audio initialization failed: {e}")
#             raise

    
#     def start_listening(self):
#         """Start listening for wake word"""
#         if self.is_listening:
#             return
            
#         self.is_listening = True
#         self.detection_thread = threading.Thread(target=self._listen_loop, daemon=True)
#         self.detection_thread.start()
#         logger.info("Wake word detection started")
    
#     def stop_listening(self):
#         """Stop wake word detection"""
#         self.is_listening = False
#         if self.detection_thread:
#             self.detection_thread.join(timeout=2.0)
#         logger.info("Wake word detection stopped")
    
#     def _listen_loop(self):
#         """Main listening loop with enhanced error handling"""
#         try:
#             import numpy as np
            
#             threshold = self.config.get("wake_word_threshold", 0.6)
#             error_count = 0
#             max_errors = 10
            
#             while self.is_listening and self.stream:
#                 try:
#                     # Read audio data with error handling
#                     try:
#                         audio_data = self.stream.read(self.chunk, exception_on_overflow=False)
#                     except TypeError:
#                         # Fallback for older PyAudio
#                         try:
#                             audio_data = self.stream.read(self.chunk)
#                         except Exception as read_error:
#                             if "Input overflowed" in str(read_error):
#                                 # Skip overflow errors and continue
#                                 continue
#                             else:
#                                 raise read_error
                    
#                     if hasattr(self, 'is_fallback'):
#                         # Fallback: simple volume detection
#                         audio_np = np.frombuffer(audio_data, dtype=np.int16)
#                         volume = np.sqrt(np.mean(audio_np**2))
                        
#                         if volume > 1000:  # Adjust threshold as needed
#                             logger.info("Volume threshold detected")
#                             if self.callback:
#                                 threading.Thread(target=self.callback, daemon=True).start()
#                             time.sleep(3)  # Prevent multiple detections
#                     else:
#                         # OpenWakeWord detection
#                         audio_np = np.frombuffer(audio_data, dtype=np.int16)
#                         predictions = self.model.predict(audio_np)
                        
#                         for wake_word in predictions:
#                             confidence = predictions[wake_word]
#                             if confidence > threshold:
#                                 logger.info(f"Wake word detected: {wake_word} (confidence: {confidence:.2f})")
#                                 if self.callback:
#                                     threading.Thread(target=self.callback, daemon=True).start()
#                                 time.sleep(2)  # Prevent multiple detections
#                                 break
                    
#                     # Reset error count on successful read
#                     error_count = 0
                        
#                 except Exception as e:
#                     error_count += 1
#                     logger.error(f"Error in detection loop ({error_count}/{max_errors}): {e}")
                    
#                     if error_count >= max_errors:
#                         logger.error("Too many audio errors, stopping detection")
#                         break
                    
#                     time.sleep(0.1)
                    
#         except Exception as e:
#             logger.error(f"Fatal error in listen loop: {e}")

    
#     def cleanup(self):
#         """Clean up resources"""
#         try:
#             self.stop_listening()
            
#             if self.stream:
#                 self.stream.stop_stream()
#                 self.stream.close()
                
#             if self.audio:
#                 self.audio.terminate()
                
#             logger.info("Wake word detector cleaned up")
            
#         except Exception as e:
#             logger.error(f"Cleanup error: {e}")
# class EightVoiceAssistant:
#     """Enhanced Voice Assistant with AI integration"""

#     def __init__(self):
#         """Initialize the complete voice assistant system"""
#         self.config = Config()
        
#         # Core components
#         self.wake_word_detector = OpenWakeWordDetector()
#         self.speech_manager = SpeechManager()
#         self.command_executor = CommandExecutor()
#         self.intent_classifier = IntentClassifier()
#         self.database_manager = DatabaseManager()
        
#         # State management
#         self.is_running = False
#         self.is_processing = False
#         self.gui = None
#         self.live_mode_active = False
#         self.conversation_context = []
        
#         # Performance metrics
#         self.start_time = time.time()
#         self.commands_processed = 0
#         self.wake_word_detections = 0
        
#         # Initialize components
#         self._initialize_system()
        
#         logger.info("Eight Voice Assistant initialized successfully")
    
#     def _initialize_system(self):
#         """Initialize all system components"""
#         try:
#             # Initialize ML model
#             self._initialize_model()
            
#             # Check API configuration
#             self._check_api_keys()
            
#             # Setup signal handlers
#             self._setup_signal_handlers()
            
#         except Exception as e:
#             logger.error(f"System initialization error: {e}")
    
#     def _initialize_model(self):
#         """Initialize the intent classification model"""
#         try:
#             # Try to load existing model
#             model = self.intent_classifier.load_model()
            
#             if not model:
#                 logger.info("Training new intent classification model...")
#                 commands, intents = self.database_manager.fetch_commands_from_db()
#                 model = self.intent_classifier.train_model(commands, intents)
#                 logger.info("Model training completed")
#             else:
#                 logger.info("Existing model loaded")
            
#         except Exception as e:
#             logger.error(f"Model initialization failed: {e}")
#             # Create fallback model
#             self.intent_classifier._create_fallback_model()
#             logger.info("Using fallback model")
    
#     def _check_api_keys(self):
#         """Check API key configuration"""
#         perplexity_key = self.config.get("perplexity_api_key")
#         gemini_key = self.config.get("gemini_api_key")
        
#         if not perplexity_key:
#             logger.warning("Perplexity API key not configured - enhanced features limited")
        
#         if not gemini_key:
#             logger.warning("Gemini API key not configured - live talk features limited")
        
#         if perplexity_key and gemini_key:
#             logger.info("API keys configured - all features available")
    
#     def _check_api_configuration(self):
#         """Check and notify GUI about API configuration"""
#         perplexity_key = self.config.get("perplexity_api_key")
#         gemini_key = self.config.get("gemini_api_key")
        
#         if not perplexity_key or not gemini_key:
#             if self.gui:
#                 self.gui.update_text("Enhanced AI features require API configuration")
#                 self.gui.update_text("Set your Perplexity and Gemini API keys in Settings")
#                 self.gui.update_text("Basic features are still available")
#         else:
#             if self.gui:
#                 self.gui.update_text("Enhanced AI features ready!")
#                 self.gui.update_text("Live Talk mode available")
#                 self.gui.update_text("Advanced search and conversation enabled")
    
#     def _setup_signal_handlers(self):
#         """Setup signal handlers for graceful shutdown"""
#         try:
#             signal.signal(signal.SIGINT, self.signal_handler)
#             signal.signal(signal.SIGTERM, self.signal_handler)
#         except Exception as e:
#             logger.warning(f"Could not setup signal handlers: {e}")
    
#     def start_gui(self):
#         """Start the graphical user interface"""
#         try:
#             logger.info("Starting GUI interface...")
            
#             self.gui = ModernVoiceAssistantGUI(
#                 start_callback=self.start_listening,
#                 stop_callback=self.stop_listening,
#                 talk_callback=self.handle_direct_command
#             )
            
#             # Display system info and API status
#             self._display_startup_info()
            
#             # Check API configuration
#             self._check_api_configuration()
            
#             # Auto-start if configured
#             if self.config.get("auto_start"):
#                 self.gui.root.after(2000, self._auto_start)
            
#             logger.info("GUI ready - starting main loop")
#             self.gui.run()
            
#         except Exception as e:
#             logger.error(f"GUI error: {e}")
#             self.cleanup()
    
#     def _display_startup_info(self):
#         """Display startup information in GUI"""
#         if self.gui:
#             uptime = time.time() - self.start_time
#             self.gui.update_text("=" * 50)
#             self.gui.update_text("EIGHT VOICE ASSISTANT v2.0")
#             self.gui.update_text("=" * 50)
#             self.gui.update_text(f"Initialization time: {uptime:.2f}s")
#             self.gui.update_text("Features: Wake Word, AI Chat, Live Talk, Research")
#             self.gui.update_text("Say 'Eight' to activate or use buttons below")
#             self.gui.update_text("=" * 50)
    
#     def _auto_start(self):
#         """Auto-start assistant if configured"""
#         try:
#             if self.config.get("auto_start") and not self.is_running:
#                 self.gui.update_text("Auto-starting assistant...")
#                 self.start_listening()
#         except Exception as e:
#             logger.error(f"Auto-start error: {e}")
    
#     def start_listening(self):
#         """Start the wake word detection system"""
#         try:
#             if self.is_running:
#                 logger.warning("Assistant already running")
#                 return
            
#             self.is_running = True
            
#             # Initialize wake word detector
#             if not self.wake_word_detector.initialize(self.on_wake_word_detected):
#                 if self.gui:
#                     self.gui.update_text("Failed to initialize wake word detection")
#                     self.gui.update_text("Check your audio device and try again")
#                 self.is_running = False
#                 return
            
#             # Start listening for wake word
#             self.wake_word_detector.start_listening()
            
#             if self.gui:
#                 self.gui.update_text(" Wake word detection started")
#                 self.gui.update_text("Say 'Eight' to activate assistant")
            
#             logger.info("Wake word detection system active")
            
#         except Exception as e:
#             logger.error(f"Failed to start listening: {e}")
#             if self.gui:
#                 self.gui.update_text(f"Error starting assistant: {str(e)}")
#             self.is_running = False
    
#     def stop_listening(self):
#         """Stop the voice assistant"""
#         try:
#             self.is_running = False
            
#             if self.wake_word_detector:
#                 self.wake_word_detector.cleanup()
            
#             if self.gui:
#                 self.gui.update_text("Voice assistant stopped")
            
#             logger.info("Voice assistant stopped")
            
#         except Exception as e:
#             logger.error(f"Error stopping assistant: {e}")
    
#     def on_wake_word_detected(self):
#         """Handle wake word detection"""
#         if self.is_processing:
#             return  # Already processing a command
        
#         self.is_processing = True
#         self.wake_word_detections += 1
        
#         try:
#             # Acknowledge wake word
#             self.speech_manager.speak("Yes, how can I help you?", interrupt=True)
            
#             if self.gui:
#                 self.gui.update_text(f"Wake word detected! (#{self.wake_word_detections})")
            
#             # Listen for user command
#             threading.Thread(target=self.listen_for_command, daemon=True).start()
            
#         except Exception as e:
#             logger.error(f"Wake word handling error: {e}")
#             if self.gui:
#                 self.gui.update_text(f" Wake word processing error: {str(e)}")
#         finally:
#             # Reset processing flag after a delay
#             threading.Timer(1.0, lambda: setattr(self, 'is_processing', False)).start()
    
#     def listen_for_command(self):
#         """Listen for and process user command"""
#         try:
#             # Get user input with timeout
#             command = self.speech_manager.listen(timeout=15)
            
#             if not command:
#                 self.speech_manager.speak("I didn't hear anything. Please try saying 'Eight' again.")
#                 return
            
#             if self.gui:
#                 self.gui.update_text(f"👤 You: {command}")
            
#             # Process the command
#             self.process_command(command)
            
#         except Exception as e:
#             logger.error(f"Command listening error: {e}")
#             self.speech_manager.speak("Sorry, I encountered an error while listening.")
#             if self.gui:
#                 self.gui.update_text(f" Listening error: {str(e)}")
    
#     def process_command(self, command):
#         """Process and execute user command with enhanced error handling"""
#         try:
#             self.commands_processed += 1
            
#             # Handle exit commands
#             exit_phrases = ['exit', 'quit', 'goodbye', 'bye', 'shutdown', 'stop assistant']
#             if any(phrase in command.lower() for phrase in exit_phrases):
#                 self._handle_exit_command()
#                 return
            
#             # Handle live mode commands
#             if 'live talk' in command.lower() or 'start live' in command.lower():
#                 response = self.handle_direct_command('start live talk')
#                 return
            
#             # Classify intent with confidence
#             intent = self.intent_classifier.classify_intent(command)
#             logger.info(f"Intent classified: '{intent}' for command: '{command}'")
            
#             # Execute command
#             response = self.command_executor.execute_command(intent, command)
            
#             # Handle empty or None responses
#             if not response or response.strip() == "":
#                 response = "I processed your request, but don't have a specific response."
            
#             # Speak response
#             self.speech_manager.speak(response)
            
#             # Update GUI with formatted response
#             if self.gui:
#                 self.gui.update_text(f" Eight: {response[:200]}{'...' if len(response) > 200 else ''}")
            
#             # Add to conversation context
#             self.conversation_context.append({
#                 "user": command,
#                 "assistant": response,
#                 "timestamp": time.time(),
#                 "intent": intent
#             })
            
#             # Keep only recent context
#             if len(self.conversation_context) > 10:
#                 self.conversation_context = self.conversation_context[-10:]
            
#             logger.info(f"Command processed successfully: {command} -> {intent}")
            
#         except Exception as e:
#             logger.error(f"Command processing error: {e}")
#             error_response = "I apologize, but I encountered an error while processing your request. Please try again."
#             self.speech_manager.speak(error_response)
            
#             if self.gui:
#                 self.gui.update_text(f" Processing error: {str(e)[:100]}...")
    
#     def _handle_exit_command(self):
#         """Handle exit/shutdown commands"""
#         try:
#             farewell_messages = [
#                 "Goodbye! Have a great day!",
#                 "See you later! Take care!",
#                 "Goodbye! It was nice talking with you!",
#                 "Until next time! Have a wonderful day!"
#             ]
            
#             import random
#             farewell = random.choice(farewell_messages)
            
#             self.speech_manager.speak(farewell)
            
#             if self.gui:
#                 self.gui.update_text(f" {farewell}")
#                 self.gui.update_text(" Assistant shutting down...")
            
#             # Graceful shutdown
#             threading.Timer(3.0, self.cleanup).start()
            
#         except Exception as e:
#             logger.error(f"Exit command error: {e}")
    
#     def handle_direct_command(self, command):
#         """Handle direct commands from GUI or conversation mode"""
#         try:
#             if not command:
#                 return "Please provide a command."
            
#             # Log the direct command
#             if self.gui:
#                 self.gui.update_text(f" Direct: {command}")
            
#             # Handle special GUI commands
#             if command == "start conversation":
#                 return self._start_conversation_mode()
#             elif command == "start live talk":
#                 return self._start_live_talk_mode()
#             elif command == "end live talk":
#                 return self._end_live_talk_mode()
            
#             # Process command directly in separate thread
#             def process_async():
#                 try:
#                     intent = self.intent_classifier.classify_intent(command)
#                     response = self.command_executor.execute_command(intent, command)
                    
#                     if response:
#                         self.speech_manager.speak(response)
#                         if self.gui:
#                             self.gui.update_text(f"Eight: {response}")
                    
#                 except Exception as e:
#                     error_msg = f"Error processing direct command: {str(e)}"
#                     if self.gui:
#                         self.gui.update_text(f"{error_msg}")
            
#             threading.Thread(target=process_async, daemon=True).start()
#             return "Processing your request..."
            
#         except Exception as e:
#             logger.error(f"Direct command error: {e}")
#             return f"Error handling command: {str(e)}"
    
#     def _start_conversation_mode(self):
#         """Start conversation mode"""
#         try:
#             if self.gui:
#                 self.gui.update_text(" Conversation mode activated")
#                 self.gui.update_text(" You can now chat naturally with Eight")
            
#             return "Conversation mode activated. What would you like to talk about?"
            
#         except Exception as e:
#             return f"Error starting conversation: {str(e)}"
    
#     def _start_live_talk_mode(self):
#         """Start live talk mode"""
#         try:
#             if self.live_mode_active:
#                 return "Live talk mode is already active."
            
#             self.live_mode_active = True
            
#             if self.gui:
#                 self.gui.update_text(" Live talk mode activated")
#                 self.gui.update_text(" Real-time conversation enabled")
            
#             # Initialize live mode if APIs are available
#             perplexity_key = self.config.get("perplexity_api_key")
#             gemini_key = self.config.get("gemini_api_key")
            
#             if perplexity_key and gemini_key:
#                 return "Live talk mode activated! You can now have real-time conversations with advanced AI capabilities."
#             else:
#                 return "Live talk mode activated with basic features. Configure API keys for enhanced capabilities."
            
#         except Exception as e:
#             logger.error(f"Live talk mode error: {e}")
#             return f"Error starting live talk: {str(e)}"
    
#     def _end_live_talk_mode(self):
#         """End live talk mode"""
#         try:
#             if not self.live_mode_active:
#                 return "Live talk mode is not active."
            
#             self.live_mode_active = False
            
#             if self.gui:
#                 self.gui.update_text(" Live talk mode ended")
            
#             return "Live talk mode ended. Returning to normal operation."
            
#         except Exception as e:
#             return f"Error ending live talk: {str(e)}"
    
#     def get_system_stats(self):
#         """Get system performance statistics"""
#         try:
#             uptime = time.time() - self.start_time
            
#             stats = {
#                 "uptime_seconds": uptime,
#                 "uptime_formatted": f"{uptime//3600:.0f}h {(uptime%3600)//60:.0f}m {uptime%60:.0f}s",
#                 "commands_processed": self.commands_processed,
#                 "wake_word_detections": self.wake_word_detections,
#                 "conversation_length": len(self.conversation_context),
#                 "is_running": self.is_running,
#                 "live_mode_active": self.live_mode_active
#             }
            
#             return stats
            
#         except Exception as e:
#             logger.error(f"Stats error: {e}")
#             return {}
    
#     def cleanup(self):
#         """Clean up resources and shutdown gracefully"""
#         try:
#             logger.info(" Starting cleanup process...")
            
#             # Stop all operations
#             self.is_running = False
#             self.live_mode_active = False
            
#             # Cleanup wake word detector
#             if self.wake_word_detector:
#                 self.wake_word_detector.cleanup()
            
#             # Display final stats
#             if self.gui:
#                 stats = self.get_system_stats()
#                 self.gui.update_text("=" * 40)
#                 self.gui.update_text("SESSION STATISTICS")
#                 self.gui.update_text(f" Uptime: {stats.get('uptime_formatted', 'Unknown')}")
#                 self.gui.update_text(f" Commands processed: {stats.get('commands_processed', 0)}")
#                 self.gui.update_text(f" Wake words detected: {stats.get('wake_word_detections', 0)}")
#                 self.gui.update_text("=" * 40)
#                 self.gui.update_text(" Cleanup completed - Safe to close")
            
#             logger.info(" Cleanup completed successfully")
            
#         except Exception as e:
#             logger.error(f"Cleanup error: {e}")
    
#     def signal_handler(self, signum, frame):
#         """Handle system signals for graceful shutdown"""
#         logger.info(f"Received signal {signum} - initiating graceful shutdown")
        
#         if self.gui:
#             self.gui.update_text(f"Received shutdown signal - cleaning up...")
        
#         self.cleanup()
        
#         # Give time for cleanup
#         time.sleep(2)
        
#         logger.info(" Exiting application")
#         sys.exit(0)

# def create_executable_instructions():
#     """Display instructions for creating executable"""
#     instructions = """
#     CREATE STANDALONE EXECUTABLE
    
#     1. Install PyInstaller:
#        pip install pyinstaller
    
#     2. Create executable:
#        pyinstaller --onefile --windowed --add-data "models;models" --add-data "config;config" main.py
    
#     3. Find executable in 'dist' folder
    
#     4. For Windows service:
#        - Use NSSM (Non-Sucking Service Manager)
#        - Or create startup shortcut in Windows startup folder
    
#     5. For auto-startup:
#        - Copy executable to: %APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup
#     """
#     print(instructions)

# def check_dependencies():
#     """Check if all required dependencies are installed"""
#     required_modules = [
#         'numpy', 'scipy', 'sklearn', 'pyaudio', 
#         'pyttsx3', 'speech_recognition', 'tkinter'
#     ]
    
#     missing_modules = []
    
#     for module in required_modules:
#         try:
#             __import__(module)
#         except ImportError:
#             missing_modules.append(module)
    
#     if missing_modules:
#         print(f" Missing required modules: {', '.join(missing_modules)}")
#         print(" Install with: pip install -r requirements.txt")
#         return False
    
#     return True

# def main():
#     """Main application entry point"""
#     try:
#         print(" Starting Eight Voice Assistant...")
#         print("=" * 50)
        
#         # Check command line arguments
#         if len(sys.argv) > 1:
#             if sys.argv[1] == "--create-exe":
#                 create_executable_instructions()
#                 return
#             elif sys.argv[1] == "--check-deps":
#                 success = check_dependencies()
#                 sys.exit(0 if success else 1)
#             elif sys.argv[1] == "--help":
#                 print("""
#                 Eight Voice Assistant - Advanced AI Voice Assistant
                
#                 Usage:
#                   python main.py                 # Start normally
#                   python main.py --create-exe    # Show executable creation instructions
#                   python main.py --check-deps    # Check dependencies
#                   python main.py --help          # Show this help
#                 """)
#                 return
        
#         # Check dependencies
#         if not check_dependencies():
#             logger.error("Missing required dependencies")
#             return
        
#         logger.info(" Starting Eight Voice Assistant v2.0")
#         logger.info(f" Python version: {sys.version}")
#         logger.info(f" Working directory: {os.getcwd()}")
        
#         # Create assistant instance
#         assistant = EightVoiceAssistant()
        
#         # Start GUI (this will block until GUI closes)
#         logger.info(" Launching GUI interface...")
#         assistant.start_gui()
        
#     except KeyboardInterrupt:
#         logger.info(" Keyboard interrupt received - shutting down gracefully")
#         if 'assistant' in locals():
#             assistant.cleanup()
#     except Exception as e:
#         logger.error(f" Fatal application error: {e}")
#         print(f" Fatal error: {e}")
#         print(" Check the log file 'eight_assistant.log' for details")
#     finally:
#         # Final cleanup
#         if 'assistant' in locals():
#             try:
#                 assistant.cleanup()
#             except:
#                 pass
        
#         logger.info(" Eight Voice Assistant shutdown complete")

# if __name__ == "__main__":
#     main()
import sys
import logging
import threading
import time
import signal
import os
import asyncio
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Enhanced logging configuration with Windows Unicode support
def setup_logging():
    """Setup logging with Windows Unicode support"""
    try:
        # Try to set UTF-8 encoding for Windows console
        if sys.platform.startswith('win'):
            os.system('chcp 65001 >nul 2>&1')  # Set console to UTF-8
    except:
        pass
    
    # Create custom formatter without emojis for file logging
    class SafeFormatter(logging.Formatter):
        def format(self, record):
            # Remove emojis from log messages for file output
            message = super().format(record)
            # Replace common emojis with text equivalents
            emoji_replacements = {
                '🚀': '[ROCKET]', '🎙️': '[MIC]', '🐍': '[PYTHON]', '📁': '[FOLDER]',
                '✅': '[SUCCESS]', '⚠️': '[WARNING]', '🧠': '[BRAIN]', '🔑': '[KEY]',
                '🎨': '[ART]', '🎯': '[TARGET]', '💻': '[COMPUTER]', '🔧': '[TOOL]',
                '📄': '[DOCUMENT]', '⚙️': '[SETTINGS]', '🌐': '[WEB]', '⏰': '[TIME]',
                '📅': '[CALENDAR]', '🔊': '[VOLUME_UP]', '🔉': '[VOLUME_DOWN]',
                '🔇': '[MUTE]', '📸': '[CAMERA]', '⌨️': '[KEYBOARD]', '🏪': '[STORE]',
                '📚': '[BOOKS]', '🌤️': '[WEATHER]', '🌡️': '[TEMPERATURE]',
                '💧': '[WATER]', '💨': '[WIND]', '❌': '[ERROR]', '❓': '[QUESTION]',
                '💬': '[CHAT]', '🛑': '[STOP]', '👤': '[USER]', '🤖': '[BOT]',
                '📊': '[STATS]', '🔍': '[SEARCH]', '📰': '[NEWS]', '💡': '[IDEA]',
                '🧹': '[CLEAN]', '👋': '[WAVE]', '💥': '[CRASH]', '📋': '[CLIPBOARD]'
            }
            
            for emoji, replacement in emoji_replacements.items():
                message = message.replace(emoji, replacement)
            
            return message
    
    # Console handler with emoji support
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # File handler with safe formatter
    file_handler = logging.FileHandler('eight_assistant.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(SafeFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[console_handler, file_handler]
    )

# Call setup_logging before any other imports
setup_logging()

# Import optimized modules
from config import Config
from speech import SpeechManager
from commands import CommandExecutor
from model import IntentClassifier
from database import DatabaseManager
from gui import ModernVoiceAssistantGUI

logger = logging.getLogger(__name__)

class OpenWakeWordDetector:
    """Enhanced wake word detector using OpenWakeWord"""
    def __init__(self):
        self.config = Config()
        self.model = None
        self.audio = None
        self.stream = None
        self.is_listening = False
        self.detection_thread = None
        self.callback = None
        
        # Audio configuration
        self.audio_format = None
        self.channels = 1
        self.rate = 16000
        self.chunk = 1024
        
        try:
            import pyaudio
            self.audio_format = pyaudio.paInt16
        except ImportError:
            logger.error("PyAudio not installed. Audio functionality limited.")
    
    def initialize(self, callback):
        """Initialize the wake word detector"""
        try:
            self.callback = callback
            
            # Use simple volume detection for now (most reliable)
            logger.info("Using simple volume-based wake word detection")
            self._initialize_audio()
            self.is_fallback = True
            return True
                
        except Exception as e:
            logger.error(f"Wake word initialization failed: {e}")
            return False
    
    def _initialize_audio(self):
        """Initialize audio stream with compatibility"""
        try:
            import pyaudio
            
            self.audio = pyaudio.PyAudio()
            
            # Simple audio stream setup for maximum compatibility
            self.stream = self.audio.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            logger.info("Audio stream initialized successfully")
            
        except Exception as e:
            logger.error(f"Audio initialization failed: {e}")
            raise
    
    def start_listening(self):
        """Start listening for wake word"""
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
            self.detection_thread.join(timeout=2.0)
        logger.info("Wake word detection stopped")
    
    def _listen_loop(self):
        """Simple volume-based detection loop"""
        try:
            import numpy as np
            
            # FIXED: Use proper default parameter
            threshold = self.config.get("wake_word_threshold", 0.6)
            detection_threshold = 3000  # Volume threshold for detection
            
            logger.info(f"Volume detection active (threshold: {detection_threshold})")
            
            while self.is_listening and self.stream:
                try:
                    # Read audio data
                    audio_data = self.stream.read(self.chunk, exception_on_overflow=False)
                    
                    # Simple volume detection
                    audio_np = np.frombuffer(audio_data, dtype=np.int16)
                    volume = np.sqrt(np.mean(audio_np**2))
                    
                    # Detect loud sounds as wake word
                    if volume > detection_threshold:
                        logger.info(f"Volume detected: {volume:.0f} > {detection_threshold}")
                        if self.callback:
                            threading.Thread(target=self.callback, daemon=True).start()
                        time.sleep(3)  # Prevent multiple detections
                        
                except Exception as e:
                    if "Input overflowed" not in str(e) and "exception_on_overflow" not in str(e):
                        logger.error(f"Audio read error: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Listen loop error: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        try:
            self.stop_listening()
            
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                
            if self.audio:
                self.audio.terminate()
                
            logger.info("Wake word detector cleaned up")
            
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

class EightVoiceAssistant:
    """Enhanced Voice Assistant with AI integration"""
    
    def __init__(self):
        """Initialize the complete voice assistant system"""
        self.config = Config()
        
        # Core components
        self.wake_word_detector = OpenWakeWordDetector()
        self.speech_manager = SpeechManager()
        self.command_executor = CommandExecutor()
        self.intent_classifier = IntentClassifier()
        self.database_manager = DatabaseManager()
        
        # State management
        self.is_running = False
        self.is_processing = False
        self.gui = None
        self.live_mode_active = False
        self.conversation_context = []
        
        # Performance metrics
        self.start_time = time.time()
        self.commands_processed = 0
        self.wake_word_detections = 0
        
        # Initialize components
        self._initialize_system()
        
        logger.info("Eight Voice Assistant initialized successfully")
    
    def _initialize_system(self):
        """Initialize all system components"""
        try:
            # Initialize ML model
            self._initialize_model()
            
            # Check API configuration
            self._check_api_keys()
            
            # Setup signal handlers
            self._setup_signal_handlers()
            
        except Exception as e:
            logger.error(f"System initialization error: {e}")
    
    def _initialize_model(self):
        """Initialize the intent classification model"""
        try:
            # Try to load existing model
            model = self.intent_classifier.load_model()
            
            if not model:
                logger.info("Training new intent classification model...")
                commands, intents = self.database_manager.fetch_commands_from_db()
                model = self.intent_classifier.train_model(commands, intents)
                logger.info("Model training completed")
            else:
                logger.info("Existing model loaded")
            
        except Exception as e:
            logger.error(f"Model initialization failed: {e}")
            # Create fallback model
            self.intent_classifier._create_fallback_model()
            logger.info("Using fallback model")
    
    def _check_api_keys(self):
        """Check API key configuration"""
        perplexity_key = self.config.get("perplexity_api_key")
        gemini_key = self.config.get("gemini_api_key")
        
        if not perplexity_key:
            logger.warning("Perplexity API key not configured - enhanced features limited")
        
        if not gemini_key:
            logger.warning("Gemini API key not configured - live talk features limited")
        
        if perplexity_key and gemini_key:
            logger.info("API keys configured - all features available")
    
    def _check_api_configuration(self):
        """Check and notify GUI about API configuration"""
        perplexity_key = self.config.get("perplexity_api_key")
        gemini_key = self.config.get("gemini_api_key")
        
        if not perplexity_key or not gemini_key:
            if self.gui:
                self.gui.update_text("Enhanced AI features require API configuration")
                self.gui.update_text("Set your Perplexity and Gemini API keys in Settings")
                self.gui.update_text("Basic features are still available")
        else:
            if self.gui:
                self.gui.update_text("Enhanced AI features ready!")
                self.gui.update_text("Live Talk mode available")
                self.gui.update_text("Advanced search and conversation enabled")
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        try:
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
        except Exception as e:
            logger.warning(f"Could not setup signal handlers: {e}")
    
    def start_gui(self):
        """Start the graphical user interface"""
        try:
            logger.info("Starting GUI interface...")
            
            self.gui = ModernVoiceAssistantGUI(
                start_callback=self.start_listening,
                stop_callback=self.stop_listening,
                talk_callback=self.handle_direct_command
            )
            
            # Display system info and API status
            self._display_startup_info()
            
            # Check API configuration
            self._check_api_configuration()
            
            # Auto-start if configured
            if self.config.get("auto_start"):
                self.gui.root.after(2000, self._auto_start)
            
            logger.info("GUI ready - starting main loop")
            self.gui.run()
            
        except Exception as e:
            logger.error(f"GUI error: {e}")
            self.cleanup()
    
    def _display_startup_info(self):
        """Display startup information in GUI"""
        if self.gui:
            uptime = time.time() - self.start_time
            self.gui.update_text("=" * 50)
            self.gui.update_text("EIGHT VOICE ASSISTANT v2.0")
            self.gui.update_text("=" * 50)
            self.gui.update_text(f"Initialization time: {uptime:.2f}s")
            self.gui.update_text("Features: Wake Word, AI Chat, Live Talk, Research")
            self.gui.update_text("Say 'Eight' LOUDLY to activate or use buttons below")
            self.gui.update_text("=" * 50)
    
    def _auto_start(self):
        """Auto-start assistant if configured"""
        try:
            if self.config.get("auto_start") and not self.is_running:
                self.gui.update_text("Auto-starting assistant...")
                self.start_listening()
        except Exception as e:
            logger.error(f"Auto-start error: {e}")
    
    def start_listening(self):
        """Start the wake word detection system"""
        try:
            if self.is_running:
                logger.warning("Assistant already running")
                return
            
            self.is_running = True
            
            # Initialize wake word detector
            if not self.wake_word_detector.initialize(self.on_wake_word_detected):
                if self.gui:
                    self.gui.update_text("Failed to initialize wake word detection")
                    self.gui.update_text("Check your audio device and try again")
                self.is_running = False
                return
            
            # Start listening for wake word
            self.wake_word_detector.start_listening()
            
            if self.gui:
                self.gui.update_text("Wake word detection started")
                self.gui.update_text("Say 'EIGHT' LOUDLY to activate assistant")
            
            logger.info("Wake word detection system active")
            
        except Exception as e:
            logger.error(f"Failed to start listening: {e}")
            if self.gui:
                self.gui.update_text(f"Error starting assistant: {str(e)}")
            self.is_running = False
    
    def stop_listening(self):
        """Stop the voice assistant"""
        try:
            self.is_running = False
            
            if self.wake_word_detector:
                self.wake_word_detector.cleanup()
            
            if self.gui:
                self.gui.update_text("Voice assistant stopped")
            
            logger.info("Voice assistant stopped")
            
        except Exception as e:
            logger.error(f"Error stopping assistant: {e}")
    
    def on_wake_word_detected(self):
        """Handle wake word detection"""
        if self.is_processing:
            return  # Already processing a command
        
        self.is_processing = True
        self.wake_word_detections += 1
        
        try:
            # Acknowledge wake word
            self.speech_manager.speak("Yes, how can I help you?", interrupt=True)
            
            if self.gui:
                self.gui.update_text(f"Wake word detected! (#{self.wake_word_detections})")
            
            # Listen for user command
            threading.Thread(target=self.listen_for_command, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Wake word handling error: {e}")
            if self.gui:
                self.gui.update_text(f"Wake word processing error: {str(e)}")
        finally:
            # Reset processing flag after a delay
            threading.Timer(2.0, lambda: setattr(self, 'is_processing', False)).start()
    
    def listen_for_command(self):
        """Listen for and process user command"""
        try:
            # Get user input with timeout
            command = self.speech_manager.listen(timeout=15)
            
            if not command:
                self.speech_manager.speak("I didn't hear anything. Please try saying 'Eight' again.")
                return
            
            if self.gui:
                self.gui.update_text(f"You: {command}")
            
            # Process the command
            self.process_command(command)
            
        except Exception as e:
            logger.error(f"Command listening error: {e}")
            self.speech_manager.speak("Sorry, I encountered an error while listening.")
            if self.gui:
                self.gui.update_text(f"Listening error: {str(e)}")
    
    def process_command(self, command):
        """Process and execute user command with enhanced error handling"""
        try:
            self.commands_processed += 1
            
            # Handle exit commands
            exit_phrases = ['exit', 'quit', 'goodbye', 'bye', 'shutdown', 'stop assistant']
            if any(phrase in command.lower() for phrase in exit_phrases):
                self._handle_exit_command()
                return
            
            # Handle live mode commands
            if 'live talk' in command.lower() or 'start live' in command.lower():
                response = self.handle_direct_command('start live talk')
                return
            
            # Classify intent with confidence
            intent = self.intent_classifier.classify_intent(command)
            logger.info(f"Intent classified: '{intent}' for command: '{command}'")
            
            # Execute command
            response = self.command_executor.execute_command(intent, command)
            
            # Handle empty or None responses
            if not response or response.strip() == "":
                response = "I processed your request, but don't have a specific response."
            
            # Speak response
            self.speech_manager.speak(response)
            
            # Update GUI with formatted response
            if self.gui:
                self.gui.update_text(f"Eight: {response[:200]}{'...' if len(response) > 200 else ''}")
            
            # Add to conversation context
            self.conversation_context.append({
                "user": command,
                "assistant": response,
                "timestamp": time.time(),
                "intent": intent
            })
            
            # Keep only recent context
            if len(self.conversation_context) > 10:
                self.conversation_context = self.conversation_context[-10:]
            
            logger.info(f"Command processed successfully: {command} -> {intent}")
            
        except Exception as e:
            logger.error(f"Command processing error: {e}")
            error_response = "I apologize, but I encountered an error while processing your request. Please try again."
            self.speech_manager.speak(error_response)
            
            if self.gui:
                self.gui.update_text(f"Processing error: {str(e)[:100]}...")
    
    def _handle_exit_command(self):
        """Handle exit/shutdown commands"""
        try:
            farewell_messages = [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Goodbye! It was nice talking with you!",
                "Until next time! Have a wonderful day!"
            ]
            
            import random
            farewell = random.choice(farewell_messages)
            
            self.speech_manager.speak(farewell)
            
            if self.gui:
                self.gui.update_text(f"{farewell}")
                self.gui.update_text("Assistant shutting down...")
            
            # Graceful shutdown
            threading.Timer(3.0, self.cleanup).start()
            
        except Exception as e:
            logger.error(f"Exit command error: {e}")
    
    def handle_direct_command(self, command):
        """Handle direct commands from GUI or conversation mode"""
        try:
            if not command:
                return "Please provide a command."
            
            # Log the direct command
            if self.gui:
                self.gui.update_text(f"Direct: {command}")
            
            # Handle special GUI commands
            if command == "start conversation":
                return self._start_conversation_mode()
            elif command == "start live talk":
                return self._start_live_talk_mode()
            elif command == "end live talk":
                return self._end_live_talk_mode()
            
            # Process command directly in separate thread
            def process_async():
                try:
                    intent = self.intent_classifier.classify_intent(command)
                    response = self.command_executor.execute_command(intent, command)
                    
                    if response:
                        self.speech_manager.speak(response)
                        if self.gui:
                            self.gui.update_text(f"Eight: {response}")
                    
                except Exception as e:
                    error_msg = f"Error processing direct command: {str(e)}"
                    if self.gui:
                        self.gui.update_text(f"{error_msg}")
            
            threading.Thread(target=process_async, daemon=True).start()
            return "Processing your request..."
            
        except Exception as e:
            logger.error(f"Direct command error: {e}")
            return f"Error handling command: {str(e)}"
    
    def _start_conversation_mode(self):
        """Start conversation mode"""
        try:
            if self.gui:
                self.gui.update_text("Conversation mode activated")
                self.gui.update_text("You can now chat naturally with Eight")
            
            return "Conversation mode activated. What would you like to talk about?"
            
        except Exception as e:
            return f"Error starting conversation: {str(e)}"
    
    def _start_live_talk_mode(self):
        """Start live talk mode"""
        try:
            if self.live_mode_active:
                return "Live talk mode is already active."
            
            self.live_mode_active = True
            
            if self.gui:
                self.gui.update_text("Live talk mode activated")
                self.gui.update_text("Real-time conversation enabled")
            
            # Initialize live mode if APIs are available
            perplexity_key = self.config.get("perplexity_api_key")
            gemini_key = self.config.get("gemini_api_key")
            
            if perplexity_key and gemini_key:
                return "Live talk mode activated! You can now have real-time conversations with advanced AI capabilities."
            else:
                return "Live talk mode activated with basic features. Configure API keys for enhanced capabilities."
                
        except Exception as e:
            logger.error(f"Live talk mode error: {e}")
            return f"Error starting live talk: {str(e)}"
    
    def _end_live_talk_mode(self):
        """End live talk mode"""
        try:
            if not self.live_mode_active:
                return "Live talk mode is not active."
            
            self.live_mode_active = False
            
            if self.gui:
                self.gui.update_text("Live talk mode ended")
            
            return "Live talk mode ended. Returning to normal operation."
            
        except Exception as e:
            return f"Error ending live talk: {str(e)}"
    
    def get_system_stats(self):
        """Get system performance statistics"""
        try:
            uptime = time.time() - self.start_time
            
            stats = {
                "uptime_seconds": uptime,
                "uptime_formatted": f"{uptime//3600:.0f}h {(uptime%3600)//60:.0f}m {uptime%60:.0f}s",
                "commands_processed": self.commands_processed,
                "wake_word_detections": self.wake_word_detections,
                "conversation_length": len(self.conversation_context),
                "is_running": self.is_running,
                "live_mode_active": self.live_mode_active
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Stats error: {e}")
            return {}
    
    def cleanup(self):
        """Clean up resources and shutdown gracefully"""
        try:
            logger.info("Starting cleanup process...")
            
            # Stop all operations
            self.is_running = False
            self.live_mode_active = False
            
            # Cleanup wake word detector
            if self.wake_word_detector:
                self.wake_word_detector.cleanup()
            
            # Display final stats
            if self.gui:
                stats = self.get_system_stats()
                self.gui.update_text("=" * 40)
                self.gui.update_text("SESSION STATISTICS")
                self.gui.update_text(f"Uptime: {stats.get('uptime_formatted', 'Unknown')}")
                self.gui.update_text(f"Commands processed: {stats.get('commands_processed', 0)}")
                self.gui.update_text(f"Wake words detected: {stats.get('wake_word_detections', 0)}")
                self.gui.update_text("=" * 40)
                self.gui.update_text("Cleanup completed - Safe to close")
            
            logger.info("Cleanup completed successfully")
            
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
    
    def signal_handler(self, signum, frame):
        """Handle system signals for graceful shutdown"""
        logger.info(f"Received signal {signum} - initiating graceful shutdown")
        
        if self.gui:
            self.gui.update_text(f"Received shutdown signal - cleaning up...")
        
        self.cleanup()
        
        # Give time for cleanup
        time.sleep(2)
        
        logger.info("Exiting application")
        sys.exit(0)

def create_executable_instructions():
    """Display instructions for creating executable"""
    instructions = """
    CREATE STANDALONE EXECUTABLE
    
    1. Install PyInstaller:
       pip install pyinstaller
    
    2. Create executable:
       pyinstaller --onefile --windowed --add-data "models;models" --add-data "config;config" main.py
    
    3. Find executable in 'dist' folder
    
    4. For Windows service:
       - Use NSSM (Non-Sucking Service Manager)
       - Or create startup shortcut in Windows startup folder
    
    5. For auto-startup:
       - Copy executable to: %APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup
    """
    print(instructions)

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_modules = [
        'numpy', 'scipy', 'sklearn', 'pyaudio', 
        'pyttsx3', 'speech_recognition', 'tkinter'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"Missing required modules: {', '.join(missing_modules)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main application entry point"""
    try:
        print("Starting Eight Voice Assistant...")
        print("=" * 50)
        
        # Check command line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] == "--create-exe":
                create_executable_instructions()
                return
            elif sys.argv[1] == "--check-deps":
                success = check_dependencies()
                sys.exit(0 if success else 1)
            elif sys.argv[1] == "--help":
                print("""
                Eight Voice Assistant - Advanced AI Voice Assistant
                
                Usage:
                  python main.py                 # Start normally
                  python main.py --create-exe    # Show executable creation instructions
                  python main.py --check-deps    # Check dependencies
                  python main.py --help          # Show this help
                """)
                return
        
        # Check dependencies
        if not check_dependencies():
            logger.error("Missing required dependencies")
            return
        
        logger.info("Starting Eight Voice Assistant v2.0")
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Working directory: {os.getcwd()}")
        
        # Create assistant instance
        assistant = EightVoiceAssistant()
        
        # Start GUI (this will block until GUI closes)
        logger.info("Launching GUI interface...")
        assistant.start_gui()
        
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received - shutting down gracefully")
        if 'assistant' in locals():
            assistant.cleanup()
    except Exception as e:
        logger.error(f"Fatal application error: {e}")
        print(f"Fatal error: {e}")
        print("Check the log file 'eight_assistant.log' for details")
    finally:
        # Final cleanup
        if 'assistant' in locals():
            try:
                assistant.cleanup()
            except:
                pass
        
        logger.info("Eight Voice Assistant shutdown complete")

if __name__ == "__main__":
    main()
