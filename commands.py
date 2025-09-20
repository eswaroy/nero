import webbrowser
import os
import subprocess
import pyautogui
import datetime
import requests
import time
import keyboard
import psutil
import logging
from pathlib import Path
from config import Config
from conversation import ConversationManager

logger = logging.getLogger(__name__)

# class CommandExecutor:
#     def __init__(self):
#         self.config = Config()
#         self.conversation_manager = ConversationManager()
#         self.chrome_path = self._find_chrome()
#         self.conversation_mode = False
        
#     def _find_chrome(self):
#         """Automatically find Chrome installation"""
#         possible_paths = [
#             "C:/Program Files/Google/Chrome/Application/chrome.exe",
#             "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
#             os.path.expanduser("~/AppData/Local/Google/Chrome/Application/chrome.exe")
#         ]
        
#         for path in possible_paths:
#             if os.path.exists(path):
#                 return f'"{path}" %s'
        
#         return None  # Use default browser if Chrome not found
    
#     def execute_command(self, intent, command=None):
#         """Enhanced command execution with error handling"""
#         try:
#             if intent == 'conversation_mode':
#                 return self.toggle_conversation_mode()
#             elif intent == 'talk' or intent == 'chat':
#                 return self.start_conversation(command)
#             elif intent == 'open_youtube':
#                 return self.open_website("https://www.youtube.com", "YouTube")
#             elif intent == 'get_time':
#                 return self.get_current_time()
#             elif intent == 'get_date':
#                 return self.get_current_date()
#             elif intent == 'open_google':
#                 return self.open_website("https://www.google.com", "Google")
#             elif intent == 'search':
#                 return self.search_web(command)
#             elif intent == 'weather':
#                 return self.get_weather_info(command)
#             elif intent == 'wikipedia':
#                 return self.search_wikipedia(command)
#             elif intent == 'system_info':
#                 return self.get_system_info()
#             elif intent == 'open_file_manager':
#                 return self.open_file_manager()
#             elif intent == 'open_settings':
#                 return self.open_settings()
#             elif intent == 'volume_up':
#                 return self.adjust_volume('up')
#             elif intent == 'volume_down':
#                 return self.adjust_volume('down')
#             elif intent == 'volume_mute':
#                 return self.toggle_mute()
#             elif intent == 'screenshot':
#                 return self.take_screenshot()
#             elif intent == 'type':
#                 return self.type_text(command)
#             elif intent == 'press_key':
#                 return self.press_key(command)
#             elif intent == 'close_application':
#                 return self.close_application(command)
#             else:
#                 # Try conversational response for unknown commands
#                 return self.conversation_manager.handle_conversation(command or intent)
                
#         except Exception as e:
#             logger.error(f"Command execution error: {e}")
#             return f"I encountered an error while executing that command: {str(e)}"
    
#     def toggle_conversation_mode(self):
#         """Toggle conversation mode on/off"""
#         self.conversation_mode = not self.conversation_mode
#         self.config.set("conversation_mode", self.conversation_mode)
        
#         if self.conversation_mode:
#             return "Conversation mode activated. I'm ready to chat about anything!"
#         else:
#             self.conversation_manager.clear_context()
#             return "Conversation mode deactivated. Back to command mode."
    
#     def start_conversation(self, query):
#         """Start or continue a conversation"""
#         if not query or query.strip() == "talk" or query.strip() == "chat":
#             self.conversation_mode = True
#             return "Hello! I'm ready to chat. What would you like to talk about?"
        
#         # Handle the query through conversation manager
#         return self.conversation_manager.handle_conversation(query)
    
#     def open_website(self, url, name):
#         """Open website with error handling"""
#         try:
#             if self.chrome_path:
#                 webbrowser.get(self.chrome_path).open(url)
#             else:
#                 webbrowser.open(url)
#             return f"Opening {name}"
#         except Exception as e:
#             return f"Sorry, I couldn't open {name}. Error: {str(e)}"
    
#     def get_current_time(self):
#         """Get current time with multiple formats"""
#         now = datetime.datetime.now()
#         time_12hr = now.strftime("%I:%M %p")
#         time_24hr = now.strftime("%H:%M")
#         return f"The current time is {time_12hr} ({time_24hr})"
    
#     def get_current_date(self):
#         """Get current date"""
#         today = datetime.datetime.now()
#         formatted_date = today.strftime("%A, %B %d, %Y")
#         return f"Today is {formatted_date}"
    
#     def search_web(self, command):
#         """Enhanced web search"""
#         if not command:
#             return "What would you like to search for?"
        
#         query = command.replace("search", "").replace("for", "").strip()
#         if not query:
#             return "Please specify what you want to search for."
        
#         try:
#             search_url = f"https://www.google.com/search?q={query}"
#             if self.chrome_path:
#                 webbrowser.get(self.chrome_path).open(search_url)
#             else:
#                 webbrowser.open(search_url)
#             return f"Searching for '{query}' on Google"
#         except Exception as e:
#             return f"Sorry, I couldn't perform the search. Error: {str(e)}"
    
#     def get_weather_info(self, command):
#         """Enhanced weather information with automatic city detection"""
#         try:
#             # Extract city from command
#             city = self._extract_city_from_command(command)
#             if not city:
#                 return "Please specify a city for weather information."
            
#             api_key = self.config.get("weather_api_key")
#             if not api_key:
#                 return "Weather service is not configured."
            
#             base_url = f"http://api.weatherapi.com/v1/current.json"
#             params = {"key": api_key, "q": city}
            
#             response = requests.get(base_url, params=params, timeout=5)
#             response.raise_for_status()
            
#             data = response.json()
            
#             if 'error' in data:
#                 return f"Weather error: {data['error']['message']}"
            
#             location = data['location']['name']
#             country = data['location']['country']
#             temp_c = data['current']['temp_c']
#             temp_f = data['current']['temp_f']
#             condition = data['current']['condition']['text']
#             humidity = data['current']['humidity']
#             wind_kph = data['current']['wind_kph']
            
#             return (f"Weather in {location}, {country}:\n"
#                    f"Temperature: {temp_c}°C ({temp_f}°F)\n"
#                    f"Condition: {condition}\n"
#                    f"Humidity: {humidity}%\n"
#                    f"Wind: {wind_kph} km/h")
            
#         except requests.exceptions.RequestException as e:
#             return f"Sorry, I couldn't fetch weather data. Please check your internet connection."
#         except Exception as e:
#             return f"Weather service error: {str(e)}"
    
#     def _extract_city_from_command(self, command):
#         """Extract city name from weather command"""
#         if not command:
#             return None
        
#         # Remove common weather-related words
#         words_to_remove = ['weather', 'in', 'for', 'at', 'of', 'the']
#         words = command.lower().split()
#         city_words = [word for word in words if word not in words_to_remove]
        
#         return ' '.join(city_words) if city_words else None
    
#     def search_wikipedia(self, command):
#         """Wikipedia search using conversation manager"""
#         query = command.replace("wikipedia", "").strip()
#         if not query:
#             return "What would you like to know about?"
        
#         return self.conversation_manager.search_wikipedia(query)
    
#     def get_system_info(self):
#         """Get system information"""
#         try:
#             cpu_percent = psutil.cpu_percent(interval=1)
#             memory = psutil.virtual_memory()
#             disk = psutil.disk_usage('/')
            
#             return (f"System Information:\n"
#                    f"CPU Usage: {cpu_percent}%\n"
#                    f"Memory Usage: {memory.percent}%\n"
#                    f"Disk Usage: {disk.percent}%\n"
#                    f"Available Memory: {memory.available // (1024**3)}GB")
#         except Exception as e:
#             return f"Couldn't retrieve system information: {str(e)}"
    
#     def open_file_manager(self):
#         """Open file manager"""
#         try:
#             if os.name == 'nt':  # Windows
#                 os.startfile('explorer')
#             else:
#                 os.system('nautilus')  # Linux
#             return "Opening File Manager"
#         except Exception as e:
#             return f"Couldn't open file manager: {str(e)}"
    
#     def open_settings(self):
#         """Open system settings"""
#         try:
#             if os.name == 'nt':  # Windows
#                 os.system("start ms-settings:")
#             else:
#                 os.system("gnome-control-center")  # Linux
#             return "Opening System Settings"
#         except Exception as e:
#             return f"Couldn't open settings: {str(e)}"
    
#     def adjust_volume(self, direction):
#         """Adjust system volume"""
#         try:
#             if direction == 'up':
#                 keyboard.press_and_release('volume up')
#                 return "Volume increased"
#             elif direction == 'down':
#                 keyboard.press_and_release('volume down')
#                 return "Volume decreased"
#         except Exception as e:
#             return f"Couldn't adjust volume: {str(e)}"
    
#     def toggle_mute(self):
#         """Toggle system mute"""
#         try:
#             keyboard.press_and_release('volume mute')
#             return "Volume muted/unmuted"
#         except Exception as e:
#             return f"Couldn't toggle mute: {str(e)}"
    
#     def take_screenshot(self):
#         """Take a screenshot"""
#         try:
#             screenshot_path = Path.home() / "Pictures" / f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
#             screenshot = pyautogui.screenshot()
#             screenshot.save(screenshot_path)
#             return f"Screenshot saved to {screenshot_path}"
#         except Exception as e:
#             return f"Couldn't take screenshot: {str(e)}"
    
#     def type_text(self, command):
#         """Type text"""
#         text = command.replace('type', '').strip()
#         if not text:
#             return "What would you like me to type?"
        
#         try:
#             pyautogui.typewrite(text)
#             return f"Typed: {text}"
#         except Exception as e:
#             return f"Couldn't type text: {str(e)}"
    
#     def press_key(self, command):
#         """Press keyboard keys"""
#         key = command.replace('press', '').strip()
#         if not key:
#             return "Which key would you like me to press?"
        
#         try:
#             pyautogui.press(key)
#             return f"Pressed {key} key"
#         except Exception as e:
#             return f"Couldn't press key: {str(e)}"
    
#     def close_application(self, command):
#         """Close application by name"""
#         app_name = command.replace('close', '').strip()
#         if not app_name:
#             return "Which application would you like to close?"
        
#         try:
#             # Map common app names to process names
#             app_mapping = {
#                 'chrome': 'chrome.exe',
#                 'firefox': 'firefox.exe',
#                 'notepad': 'notepad.exe',
#                 'calculator': 'calc.exe'
#             }
            
#             process_name = app_mapping.get(app_name.lower(), f"{app_name}.exe")
            
#             for proc in psutil.process_iter(['pid', 'name']):
#                 if proc.info['name'].lower() == process_name.lower():
#                     proc.terminate()
#                     return f"Closed {app_name}"
            
#             return f"Couldn't find {app_name} running"
            
#         except Exception as e:
#             return f"Couldn't close application: {str(e)}"
import webbrowser
import os
import subprocess
import pyautogui
import datetime
import requests
import wikipedia
import pyperclip
import time
import keyboard
import psutil
import logging
import threading
import asyncio
import json
import re
import random
from pathlib import Path
from typing import Optional, Dict, Any, List
from config import Config

# Configure logging
logger = logging.getLogger(__name__)

class EnhancedAPIManager:
    """Enhanced API Manager for Perplexity and Gemini integration"""
    
    def __init__(self, perplexity_key: str, gemini_key: str):
        self.perplexity_key = perplexity_key
        self.gemini_key = gemini_key
        self.conversation_context = []
        self.live_mode_active = False
        
        # Initialize API clients
        self._initialize_apis()
    
    def _initialize_apis(self):
        """Initialize API clients"""
        try:
            # Initialize Perplexity client
            if self.perplexity_key:
                import openai
                self.perplexity_client = openai.OpenAI(
                    api_key=self.perplexity_key,
                    base_url="https://api.perplexity.ai"
                )
                logger.info(" Perplexity API initialized")
            else:
                self.perplexity_client = None
                logger.warning(" Perplexity API key not provided")
            
            # Initialize Gemini client
            if self.gemini_key:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=self.gemini_key)
                    self.gemini_model = genai.GenerativeModel('gemini-pro')
                    logger.info(" Gemini API initialized")
                except ImportError:
                    self.gemini_model = None
                    logger.warning(" Google GenerativeAI not installed")
            else:
                self.gemini_model = None
                logger.warning(" Gemini API key not provided")
                
        except Exception as e:
            logger.error(f"API initialization error: {e}")
            self.perplexity_client = None
            self.gemini_model = None
    
    def smart_query_router(self, query: str) -> tuple[str, str]:
        """Intelligently route queries to appropriate API"""
        query_lower = query.lower()
        
        # Real-time/current information keywords
        current_info_keywords = [
            'news', 'latest', 'current', 'today', 'recent', 'now', 
            'weather', 'stock', 'price', 'happening', 'update'
        ]
        
        # Conversational keywords
        conversation_keywords = [
            'chat', 'talk', 'discuss', 'conversation', 'tell me',
            'what do you think', 'opinion', 'advice', 'help me'
        ]
        
        # Research keywords
        research_keywords = [
            'analyze', 'research', 'compare', 'explain', 'deep dive',
            'comprehensive', 'detailed', 'study', 'investigation'
        ]
        
        # Technical keywords
        technical_keywords = [
            'code', 'programming', 'technical', 'algorithm', 'debug',
            'software', 'development', 'api', 'database'
        ]
        
        if any(keyword in query_lower for keyword in current_info_keywords):
            return "perplexity_news", query
        elif any(keyword in query_lower for keyword in research_keywords):
            return "perplexity_research", query
        elif any(keyword in query_lower for keyword in technical_keywords):
            return "gemini_technical", query
        elif any(keyword in query_lower for keyword in conversation_keywords):
            return "gemini_chat", query
        else:
            # Default routing based on API availability
            if self.perplexity_client:
                return "perplexity_search", query
            elif self.gemini_model:
                return "gemini_chat", query
            else:
                return "fallback", query
    
    def process_query(self, query: str) -> str:
        """Process query through appropriate API"""
        try:
            route, processed_query = self.smart_query_router(query)
            
            if route == "perplexity_news":
                return self._perplexity_news_search(processed_query)
            elif route == "perplexity_research":
                return self._perplexity_research(processed_query)
            elif route == "perplexity_search":
                return self._perplexity_search(processed_query)
            elif route == "gemini_technical":
                return self._gemini_technical_help(processed_query)
            elif route == "gemini_chat":
                return self._gemini_conversation(processed_query)
            else:
                return self._fallback_response(processed_query)
                
        except Exception as e:
            logger.error(f"Query processing error: {e}")
            return f"I encountered an error while processing your query: {str(e)}"
    
    # def _perplexity_search(self, query: str) -> str:
    #     """General search with Perplexity"""
    #     try:
    #         if not self.perplexity_client:
    #             return "Perplexity API is not available."
            
    #         messages = [
    #             {"role": "user", "content": f"Please provide comprehensive information about: {query}"}
    #         ]
            
    #         # Add conversation context
    #         if self.conversation_context:
    #             context_msg = "Previous conversation context:\n"
    #             for msg in self.conversation_context[-3:]:
    #                 context_msg += f"User: {msg.get('user', '')}\nAssistant: {msg.get('assistant', '')}\n"
    #             messages.insert(0, {"role": "system", "content": context_msg})
            
    #         response = self.perplexity_client.chat.completions.create(
    #             model="llama-3.1-sonar-small-128k-online",
    #             messages=messages,
    #             temperature=0.2,
    #             max_tokens=2000
    #         )
            
    #         return response.choices[0].message.content
            
    #     except Exception as e:
    #         logger.error(f"Perplexity search error: {e}")
    #         return f"Search error: {str(e)}"
    
    # def _perplexity_news_search(self, query: str) -> str:
    #     """Get latest news with Perplexity"""
    #     try:
    #         if not self.perplexity_client:
    #             return "News search requires Perplexity API."
            
    #         topic = query.replace("news", "").replace("latest", "").strip()
    #         search_query = f"Latest news about {topic}" if topic else "Latest news today"
            
    #         response = self.perplexity_client.chat.completions.create(
    #             model="llama-3.1-sonar-small-128k-online",
    #             messages=[{
    #                 "role": "user",
    #                 "content": f"Give me the top 5 latest news stories about {search_query}. Include dates, sources, and brief summaries."
    #             }],
    #             temperature=0.1,
    #             max_tokens=1500
    #         )
            
    #         return response.choices[0].message.content
            
    #     except Exception as e:
    #         return f"News fetch error: {str(e)}"
    
    # def _perplexity_research(self, query: str) -> str:
    #     """Deep research with Perplexity"""
    #     try:
    #         if not self.perplexity_client:
    #             return "Research requires Perplexity API."
            
    #         response = self.perplexity_client.chat.completions.create(
    #             model="llama-3.1-sonar-small-128k-online",
    #             messages=[{
    #                 "role": "system",
    #                 "content": "You are a research assistant. Provide detailed, well-researched answers with current information, multiple perspectives, and credible sources."
    #             }, {
    #                 "role": "user",
    #                 "content": query
    #             }],
    #             temperature=0.3,
    #             max_tokens=3000
    #         )
            
    #         return response.choices[0].message.content
            
    #     except Exception as e:
    #         return f"Research error: {str(e)}"
    def _perplexity_search(self, query: str) -> str:
        """General search with Perplexity"""
        try:
            if not self.perplexity_client:
                return "Perplexity API is not available."
            
            messages = [
                {"role": "user", "content": f"Please provide comprehensive information about: {query}"}
            ]
            
            response = self.perplexity_client.chat.completions.create(
                model="sonar",  # CORRECTED: Use simple model name
                messages=messages,
                temperature=0.2,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Perplexity search error: {e}")
            # Fallback to basic response
            return f"I understand you're asking about '{query}'. Let me help with basic information: This appears to be a query that would benefit from current web search. Please configure your Perplexity API key for enhanced results."
    
    def _perplexity_news_search(self, query: str) -> str:
        """Get latest news with Perplexity"""
        try:
            if not self.perplexity_client:
                return "News search requires Perplexity API."
            
            response = self.perplexity_client.chat.completions.create(
                model="sonar",  # CORRECTED: Use simple model name
                messages=[{
                    "role": "user",
                    "content": f"Give me the latest news about {query}. Include sources."
                }],
                temperature=0.1,
                max_tokens=800
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"News search error: {e}")
            return f"News search temporarily unavailable. Please check your Perplexity API configuration."
    
    def _perplexity_research(self, query: str) -> str:
        """Deep research with Perplexity"""
        try:
            if not self.perplexity_client:
                return "Research requires Perplexity API."
            
            response = self.perplexity_client.chat.completions.create(
                model="sonar-pro",  # CORRECTED: Use correct pro model name
                messages=[{
                    "role": "system",
                    "content": "Provide detailed research with sources and current information."
                }, {
                    "role": "user",
                    "content": query
                }],
                temperature=0.3,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Research error: {e}")
            return f"Research temporarily unavailable. Basic info: {query} - Please configure your Perplexity API for detailed research."


    
    def _gemini_conversation(self, query: str) -> str:
        """Conversational response with Gemini"""
        try:
            if not self.gemini_model:
                return "Conversation mode requires Gemini API."
            
            # Build conversation context
            full_prompt = query
            if self.conversation_context:
                context = "\n".join([
                    f"User: {msg.get('user', '')}\nAssistant: {msg.get('assistant', '')}" 
                    for msg in self.conversation_context[-3:]
                ])
                full_prompt = f"Previous conversation:\n{context}\n\nCurrent question: {query}"
            
            response = self.gemini_model.generate_content(full_prompt)
            
            # Update conversation context
            self.conversation_context.append({
                "user": query,
                "assistant": response.text,
                "timestamp": time.time()
            })
            
            # Keep only recent context
            if len(self.conversation_context) > 10:
                self.conversation_context = self.conversation_context[-10:]
            
            return response.text
            
        except Exception as e:
            return f"Conversation error: {str(e)}"
    
    def _gemini_technical_help(self, query: str) -> str:
        """Technical assistance with Gemini"""
        try:
            if not self.gemini_model:
                return "Technical help requires Gemini API."
            
            technical_prompt = f"""
            You are a technical assistant. Please help with this technical query: {query}
            
            Provide:
            1. Clear explanation
            2. Code examples if applicable
            3. Best practices
            4. Common pitfalls to avoid
            """
            
            response = self.gemini_model.generate_content(technical_prompt)
            return response.text
            
        except Exception as e:
            return f"Technical help error: {str(e)}"
    
    def _fallback_response(self, query: str) -> str:
        """Fallback response when APIs are unavailable"""
        fallback_responses = [
            f"I understand you're asking about '{query}'. However, I need API access for detailed responses.",
            f"Your query about '{query}' is interesting, but I require enhanced features to provide a comprehensive answer.",
            f"I'd love to help with '{query}', but this requires API configuration for advanced capabilities."
        ]
        
        return random.choice(fallback_responses)

class CommandExecutor:
    """Enhanced Command Executor with AI integration"""
    
    def __init__(self):
        self.config = Config()
        self.chrome_path = self._find_chrome()
        self.conversation_mode = False
        self.live_mode_active = False
        self.command_history = []
        
        # Initialize API manager if keys are available
        perplexity_key = self.config.get("perplexity_api_key")
        gemini_key = self.config.get("gemini_api_key")
        
        if perplexity_key and gemini_key:
            try:
                self.api_manager = EnhancedAPIManager(perplexity_key, gemini_key)
                logger.info(" Enhanced API manager initialized")
            except Exception as e:
                logger.error(f"API manager initialization failed: {e}")
                self.api_manager = None
        else:
            logger.warning(" API keys not configured - basic features only")
            self.api_manager = None
        
        # Fallback conversation manager
        self.fallback_conversation = self._initialize_fallback()
    
    def _initialize_fallback(self):
        """Initialize fallback conversation system"""
        try:
            from conversation import ConversationManager
            return ConversationManager()
        except ImportError:
            logger.warning("Conversation module not available")
            return None
    
    def _find_chrome(self):
        """Automatically find Chrome installation"""
        possible_paths = [
            "C:/Program Files/Google/Chrome/Application/chrome.exe",
            "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
            os.path.expanduser("~/AppData/Local/Google/Chrome/Application/chrome.exe"),
            "/usr/bin/google-chrome",
            "/usr/bin/chromium-browser"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return f'"{path}" %s' if " " in path else f'{path} %s'
        
        logger.warning("Chrome not found, using default browser")
        return None
    
    def execute_command(self, intent, command=None):
        """Enhanced command execution with comprehensive error handling"""
        try:
            # Log command for analytics
            self.command_history.append({
                "intent": intent,
                "command": command,
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            # Keep only recent history
            if len(self.command_history) > 100:
                self.command_history = self.command_history[-100:]
            
            logger.info(f"Executing command - Intent: {intent}, Command: {command}")
            
            # Live conversation commands
            if intent == 'start_live_talk' or (command and 'live talk' in command.lower()):
                return self.start_live_conversation()
            elif intent == 'end_live_talk' or (command and 'end live' in command.lower()):
                return self.end_live_conversation()
            
            # Enhanced AI commands
            elif intent == 'ai_chat' or intent == 'talk' or intent == 'ask_ai':
                return self.handle_ai_conversation(command)
            elif intent == 'get_news':
                return self.get_latest_news(command)
            elif intent == 'research' or intent == 'analyze':
                return self.handle_research_query(command)
            elif intent == 'technical_help':
                return self.handle_technical_query(command)
            
            # Enhanced existing commands
            elif intent == 'weather':
                return self.get_enhanced_weather(command)
            elif intent == 'wikipedia':
                return self.get_enhanced_wikipedia(command)
            elif intent == 'search':
                return self.enhanced_web_search(command)
            
            # System and application commands
            elif intent == 'open_youtube' or intent == 'open_YouTube':
                return self.open_website("https://www.youtube.com", "YouTube")
            elif intent == 'get_time':
                return self.get_current_time()
            elif intent == 'get_date':
                return self.get_current_date()
            elif intent == 'open_google':
                return self.open_website("https://www.google.com", "Google")
            elif intent == 'system_info':
                return self.get_system_info()
            elif intent == 'open_file_manager':
                return self.open_file_manager()
            elif intent == 'screenshot':
                return self.take_screenshot()
            elif intent == 'volume_up':
                return self.adjust_volume('up')
            elif intent == 'volume_down':
                return self.adjust_volume('down')
            elif intent == 'volume_mute':
                return self.toggle_mute()
            
            # Microsoft Office applications
            elif intent == 'open_word':
                return self.open_office_app("word", "Word")
            elif intent == 'open_excel':
                return self.open_office_app("excel", "Excel")
            elif intent == 'open_powerpoint':
                return self.open_office_app("powerpnt", "PowerPoint")
            elif intent == 'open_one_note' or intent == 'open_onenote':
                return self.open_office_app("onenote", "OneNote")
            
            # Windows settings
            elif intent == 'open_settings':
                return self.open_windows_settings()
            elif intent == 'open_network_settings':
                return self.open_windows_settings("network")
            elif intent == 'open_bluetooth_settings':
                return self.open_windows_settings("bluetooth")
            elif intent == 'open_privacy_settings':
                return self.open_windows_settings("privacy")
            
            # Automation commands
            elif intent == 'type':
                return self.type_text(command)
            elif intent == 'press' or intent.startswith('press_'):
                return self.press_key(command, intent)
            elif intent == 'close_google' or intent == 'close_chrome':
                return self.close_application("chrome")
            elif intent.startswith('close_'):
                app_name = intent.replace('close_', '')
                return self.close_application(app_name)
            
            # Chat applications
            elif intent == 'open_chatgpt':
                return self.open_website("https://chat.openai.com", "ChatGPT")
            elif intent == 'open_microsoft_store':
                return self.open_microsoft_store()
            
            else:
                # Enhanced fallback with AI
                return self.handle_unknown_command(command or intent)
                
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return f"I encountered an error while executing that command: {str(e)}"
    
    # AI-Enhanced Command Methods
    
    def start_live_conversation(self):
        """Start live conversation mode"""
        try:
            if self.live_mode_active:
                return "Live conversation mode is already active."
            
            self.live_mode_active = True
            
            if self.api_manager:
                return "🎙️ Live conversation mode activated! You can now have real-time conversations with advanced AI capabilities. Ask me anything!"
            else:
                return "🎙️ Live conversation mode activated with basic features. Configure Perplexity and Gemini API keys for enhanced capabilities."
                
        except Exception as e:
            logger.error(f"Live conversation start error: {e}")
            return f"Failed to start live conversation: {str(e)}"
    
    def end_live_conversation(self):
        """End live conversation mode"""
        try:
            if not self.live_mode_active:
                return "Live conversation mode is not currently active."
            
            self.live_mode_active = False
            return "🛑 Live conversation mode ended. Returning to normal command mode."
            
        except Exception as e:
            return f"Error ending live conversation: {str(e)}"
    
    def handle_ai_conversation(self, query):
        """Handle AI-powered conversation"""
        try:
            if not query or query.strip() == "":
                return "What would you like to talk about? I'm here to help with questions, research, or just have a conversation!"
            
            if self.api_manager:
                # Use enhanced API manager for intelligent routing
                response = self.api_manager.process_query(query)
                return response
            elif self.fallback_conversation:
                # Use fallback conversation manager
                return self.fallback_conversation.handle_conversation(query)
            else:
                return "I'd love to chat, but I need API configuration for advanced conversation features. I can still help with basic commands though!"
                
        except Exception as e:
            logger.error(f"AI conversation error: {e}")
            return f"I encountered an error during our conversation: {str(e)}"
    
    def get_latest_news(self, query):
        """Get latest news with AI enhancement"""
        try:
            if self.api_manager:
                topic = None
                if query:
                    # Extract topic from query
                    topic = query.replace("news", "").replace("latest", "").replace("about", "").strip()
                
                return self.api_manager._perplexity_news_search(query or "latest news")
            else:
                return "📰 News service requires Perplexity API key configuration. Please set up your API keys in settings."
                
        except Exception as e:
            return f"News fetch error: {str(e)}"
    
    def handle_research_query(self, query):
        """Handle deep research queries"""
        try:
            if not query:
                return "What topic would you like me to research for you?"
            
            if self.api_manager:
                return self.api_manager._perplexity_research(query)
            else:
                return "🔍 Research service requires Perplexity API key configuration."
                
        except Exception as e:
            return f"Research error: {str(e)}"
    
    def handle_technical_query(self, query):
        """Handle technical assistance queries"""
        try:
            if not query:
                return "What technical topic can I help you with?"
            
            if self.api_manager:
                return self.api_manager._gemini_technical_help(query)
            else:
                return "💻 Technical assistance requires Gemini API key configuration."
                
        except Exception as e:
            return f"Technical help error: {str(e)}"
    
    # Enhanced Existing Commands
    
    def get_enhanced_weather(self, command):
        """Enhanced weather with AI insights"""
        try:
            # Get basic weather first
            basic_weather = self.get_weather_info(command)
            
            if self.api_manager and "error" not in basic_weather.lower():
                # Enhance with AI insights
                city = self._extract_city_from_command(command)
                if city:
                    ai_query = f"Based on current weather in {city}, what recommendations do you have for activities, clothing, or precautions?"
                    ai_insights = self.api_manager.process_query(ai_query)
                    return f"{basic_weather}\n\n🤖 AI Recommendations:\n{ai_insights[:300]}..."
            
            return basic_weather
            
        except Exception as e:
            return f"Enhanced weather error: {str(e)}"
    
    def get_enhanced_wikipedia(self, command):
        """Enhanced Wikipedia with AI summary"""
        try:
            query = command.replace("wikipedia", "").replace("about", "").strip()
            
            if not query:
                return "What topic would you like me to look up on Wikipedia?"
            
            if self.api_manager:
                # Use AI-powered search for more comprehensive results
                enhanced_response = self.api_manager.process_query(f"Provide comprehensive information about {query}")
                return enhanced_response
            elif self.fallback_conversation:
                return self.fallback_conversation.search_wikipedia(query)
            else:
                # Basic Wikipedia fallback
                return self.basic_wikipedia_search(query)
                
        except Exception as e:
            return f"Enhanced Wikipedia error: {str(e)}"
    
    def enhanced_web_search(self, command):
        """Enhanced web search with AI"""
        try:
            search_query = command.replace("search", "").replace("for", "").strip()
            
            if not search_query:
                return "What would you like me to search for?"
            
            # Open search in browser
            search_url = f"https://www.google.com/search?q={search_query}"
            if self.chrome_path:
                webbrowser.get(self.chrome_path).open(search_url)
            else:
                webbrowser.open(search_url)
            
            # Provide AI-enhanced summary if available
            if self.api_manager:
                try:
                    summary = self.api_manager.process_query(f"Briefly summarize key information about: {search_query}")
                    return f"🔍 Opened search for '{search_query}' in browser.\n\n📋 Quick Summary:\n{summary[:200]}..."
                except:
                    pass
            
            return f"🔍 Searching for '{search_query}' on Google"
            
        except Exception as e:
            return f"Search error: {str(e)}"
    
    # System and Application Commands
    
    def open_website(self, url, name):
        """Open website with error handling"""
        try:
            if self.chrome_path:
                webbrowser.get(self.chrome_path).open(url)
            else:
                webbrowser.open(url)
            return f"🌐 Opening {name}"
        except Exception as e:
            return f"Sorry, I couldn't open {name}. Error: {str(e)}"
    
    def get_current_time(self):
        """Get current time with multiple formats"""
        try:
            now = datetime.datetime.now()
            time_12hr = now.strftime("%I:%M %p")
            time_24hr = now.strftime("%H:%M")
            date_str = now.strftime("%A, %B %d, %Y")
            return f"⏰ The current time is {time_12hr} ({time_24hr}) on {date_str}"
        except Exception as e:
            return f"Time error: {str(e)}"
    
    def get_current_date(self):
        """Get current date with additional info"""
        try:
            today = datetime.datetime.now()
            formatted_date = today.strftime("%A, %B %d, %Y")
            day_of_year = today.timetuple().tm_yday
            week_number = today.isocalendar()[1]
            return f"📅 Today is {formatted_date} (Day {day_of_year} of the year, Week {week_number})"
        except Exception as e:
            return f"Date error: {str(e)}"
    
    def get_system_info(self):
        """Get comprehensive system information"""
        try:
            import platform
            
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.datetime.now() - boot_time
            
            system_info = f"""💻 System Information:
🖥️ OS: {platform.system()} {platform.release()}
🔧 CPU Usage: {cpu_percent}%
🧠 Memory: {memory.percent}% used ({memory.available // (1024**3)}GB available)
💾 Disk: {disk.percent}% used
⏱️ Uptime: {str(uptime).split('.')[0]}
🔋 Battery: {"N/A" if not hasattr(psutil, "sensors_battery") or not psutil.sensors_battery() else f"{psutil.sensors_battery().percent}%"}"""
            
            return system_info
            
        except Exception as e:
            return f"Couldn't retrieve system information: {str(e)}"
    
    def open_file_manager(self):
        """Open file manager with smart detection"""
        try:
            system = os.name
            if system == 'nt':  # Windows
                os.startfile('explorer')
            elif system == 'posix':  # Unix/Linux/macOS
                if os.uname().sysname == 'Darwin':  # macOS
                    os.system('open .')
                else:  # Linux
                    os.system('nautilus . || dolphin . || thunar . || pcmanfm .')
            
            return "📁 Opening File Manager"
        except Exception as e:
            return f"Couldn't open file manager: {str(e)}"
    
    def open_office_app(self, app_name, display_name):
        """Open Microsoft Office applications intelligently"""
        try:
            # Try different methods to open Office apps
            methods = [
                f"start {app_name}",
                f"start ms-{app_name}:",
                f"start {app_name}.exe"
            ]
            
            for method in methods:
                try:
                    os.system(method)
                    return f"📄 Opening {display_name}"
                except:
                    continue
            
            # Fallback: try to find in common locations
            common_paths = [
                f"C:\\Program Files\\Microsoft Office\\root\\Office16\\{app_name.upper()}.EXE",
                f"C:\\Program Files (x86)\\Microsoft Office\\Office16\\{app_name.upper()}.EXE"
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    os.startfile(path)
                    return f"📄 Opening {display_name}"
            
            return f"❌ {display_name} not found. Please install Microsoft Office."
            
        except Exception as e:
            return f"Couldn't open {display_name}: {str(e)}"
    
    def open_windows_settings(self, setting_type=None):
        """Open Windows settings with specific categories"""
        try:
            if setting_type:
                os.system(f"start ms-settings:{setting_type}")
                return f"⚙️ Opening {setting_type.title()} Settings"
            else:
                os.system("start ms-settings:")
                return "⚙️ Opening Windows Settings"
        except Exception as e:
            return f"Couldn't open settings: {str(e)}"
    
    def open_microsoft_store(self):
        """Open Microsoft Store"""
        try:
            os.system("start ms-windows-store:")
            return "🏪 Opening Microsoft Store"
        except Exception as e:
            return f"Couldn't open Microsoft Store: {str(e)}"
    
    # Automation Commands
    
    def type_text(self, command):
        """Type text with enhanced features"""
        try:
            text = command.replace('type', '').strip()
            if not text:
                return "What would you like me to type?"
            
            # Add small delay for reliability
            time.sleep(0.5)
            pyautogui.typewrite(text, interval=0.05)
            return f"⌨️ Typed: {text}"
        except Exception as e:
            return f"Couldn't type text: {str(e)}"
    
    def press_key(self, command, intent):
        """Press keyboard keys with intelligent parsing"""
        try:
            # Extract key from command or intent
            if intent.startswith('press_'):
                key = intent.replace('press_', '')
            else:
                key = command.replace('press', '').strip() if command else ''
            
            if not key:
                return "Which key would you like me to press?"
            
            # Handle special key mappings
            key_mappings = {
                'enter': 'enter',
                'return': 'enter',
                'space': 'space',
                'spacebar': 'space',
                'tab': 'tab',
                'escape': 'esc',
                'esc': 'esc',
                'delete': 'del',
                'backspace': 'backspace'
            }
            
            actual_key = key_mappings.get(key.lower(), key.lower())
            pyautogui.press(actual_key)
            return f"⌨️ Pressed {key} key"
        except Exception as e:
            return f"Couldn't press key: {str(e)}"
    
    def take_screenshot(self):
        """Take screenshot with automatic naming"""
        try:
            # Create screenshots directory if it doesn't exist
            screenshots_dir = Path.home() / "Pictures" / "Eight_Screenshots"
            screenshots_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_path = screenshots_dir / f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            
            return f"📸 Screenshot saved to {screenshot_path}"
        except Exception as e:
            return f"Couldn't take screenshot: {str(e)}"
    
    # Audio Control
    
    def adjust_volume(self, direction):
        """Adjust system volume"""
        try:
            if direction == 'up':
                keyboard.press_and_release('volume up')
                return "🔊 Volume increased"
            elif direction == 'down':
                keyboard.press_and_release('volume down')
                return "🔉 Volume decreased"
        except Exception as e:
            return f"Couldn't adjust volume: {str(e)}"
    
    def toggle_mute(self):
        """Toggle system mute"""
        try:
            keyboard.press_and_release('volume mute')
            return "🔇 Volume toggled (mute/unmute)"
        except Exception as e:
            return f"Couldn't toggle mute: {str(e)}"
    
    # Application Management
    
    def close_application(self, app_name):
        """Close application by name with smart detection"""
        try:
            # App name mappings
            app_mappings = {
                'chrome': ['chrome.exe', 'google chrome'],
                'firefox': ['firefox.exe'],
                'edge': ['msedge.exe', 'microsoft edge'],
                'notepad': ['notepad.exe'],
                'calculator': ['calc.exe', 'calculator.exe'],
                'word': ['winword.exe', 'microsoft word'],
                'excel': ['excel.exe', 'microsoft excel'],
                'powerpoint': ['powerpnt.exe', 'microsoft powerpoint']
            }
            
            process_names = app_mappings.get(app_name.lower(), [f"{app_name}.exe"])
            
            closed_processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    if any(target.lower() in proc_name for target in process_names):
                        proc.terminate()
                        closed_processes.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if closed_processes:
                return f"✅ Closed: {', '.join(closed_processes)}"
            else:
                return f"❌ No running instances of {app_name} found"
                
        except Exception as e:
            return f"Couldn't close {app_name}: {str(e)}"
    
    # Weather and Information Services
    
    def get_weather_info(self, command):
        """Enhanced weather information"""
        try:
            city = self._extract_city_from_command(command) if command else None
            
            if not city:
                return "Please specify a city for weather information. For example: 'weather in London' or 'weather Mumbai'"
            
            api_key = self.config.get("weather_api_key", "30fb90a564464659a2d134443242508")
            base_url = f"http://api.weatherapi.com/v1/current.json"
            params = {"key": api_key, "q": city, "aqi": "yes"}
            
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'error' in data:
                return f"Weather error: {data['error']['message']}"
            
            location = data['location']['name']
            country = data['location']['country']
            temp_c = data['current']['temp_c']
            temp_f = data['current']['temp_f']
            condition = data['current']['condition']['text']
            humidity = data['current']['humidity']
            wind_kph = data['current']['wind_kph']
            feels_like_c = data['current']['feelslike_c']
            
            weather_info = f"""🌤️ Weather in {location}, {country}:
🌡️ Temperature: {temp_c}°C ({temp_f}°F)
🤔 Feels like: {feels_like_c}°C
☁️ Condition: {condition}
💧 Humidity: {humidity}%
💨 Wind: {wind_kph} km/h"""
            
            return weather_info
            
        except requests.exceptions.RequestException:
            return "❌ Unable to fetch weather data. Please check your internet connection."
        except Exception as e:
            return f"Weather service error: {str(e)}"
    
    def _extract_city_from_command(self, command):
        """Extract city name from weather command"""
        if not command:
            return None
        
        # Remove common weather-related words
        words_to_remove = ['weather', 'in', 'for', 'at', 'of', 'the', 'what', 'is', 'show', 'me']
        words = command.lower().split()
        city_words = [word for word in words if word not in words_to_remove]
        
        return ' '.join(city_words) if city_words else None
    
    # Fallback Methods
    
    def basic_wikipedia_search(self, query):
        """Basic Wikipedia search fallback"""
        try:
            if not query:
                return "Please provide a topic to search on Wikipedia."
            
            results = wikipedia.summary(query, sentences=3)
            return f"📚 According to Wikipedia:\n\n{results}"
            
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options[:5]
            return f"Multiple results found for '{query}'. Did you mean: {', '.join(options)}?"
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for '{query}'. Please try a different search term."
        except Exception as e:
            return f"Wikipedia search error: {str(e)}"
    
    def handle_unknown_command(self, command):
        """Enhanced unknown command handling"""
        try:
            if self.api_manager:
                # Let AI handle unknown commands
                response = self.api_manager.process_query(f"The user said: '{command}'. Please help them or suggest what they might be looking for.")
                return response
            elif self.fallback_conversation:
                return self.fallback_conversation.handle_conversation(command)
            else:
                suggestions = [
                    "Try: 'what time is it', 'open YouTube', 'weather in [city]'",
                    "Say: 'take screenshot', 'search for [topic]', 'news about [topic]'",
                    "Ask: 'system info', 'talk to me', or 'help'"
                ]
                
                return f"❓ I'm not sure how to handle '{command}'. {random.choice(suggestions)}"
                
        except Exception as e:
            return f"Error processing command: {str(e)}"
    
    def get_command_statistics(self):
        """Get command usage statistics"""
        try:
            if not self.command_history:
                return "No commands executed yet."
            
            # Analyze command history
            intent_counts = {}
            for cmd in self.command_history:
                intent = cmd['intent']
                intent_counts[intent] = intent_counts.get(intent, 0) + 1
            
            # Get top 5 commands
            top_commands = sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            stats = f"""📊 Command Statistics:
📈 Total commands: {len(self.command_history)}
🏆 Top commands: {', '.join([f"{cmd}({count})" for cmd, count in top_commands])}
⏰ Latest: {self.command_history[-1]['timestamp'] if self.command_history else 'None'}"""
            
            return stats
            
        except Exception as e:
            return f"Statistics error: {str(e)}"


# Legacy function wrapper for compatibility
def execute_command(intent, command=None):
    """Legacy wrapper function for backward compatibility"""
    executor = CommandExecutor()
    return executor.execute_command(intent, command)
