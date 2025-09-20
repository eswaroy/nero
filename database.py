import json
import logging
from pathlib import Path
from config import Config
import datetime
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.config = Config()
        self.data_file = self.config.config_dir / "commands_data.json"
        self.fallback_data = self._create_fallback_data()
        
    def _create_fallback_data(self):
        """Create fallback training data"""
        return {
            "commands": [
                # YouTube commands
                "open youtube", "play youtube", "youtube", "video",
                
                # Time commands
                "what time is it", "current time", "time", "what's the time",
                
                # Google/Search commands
                "open google", "search", "google search", "look up",
                
                # Weather commands
                "weather", "what's the weather", "weather forecast", "climate",
                
                # Wikipedia commands
                "wikipedia", "tell me about", "what is", "who is",
                
                # Conversation commands
                "talk", "chat", "let's talk", "conversation",
                
                # System commands
                "screenshot", "take screenshot", "capture", "snap",
                "open file manager", "files", "explorer", "folder",
                "system info", "computer stats", "performance",
                "volume up", "increase volume", "louder",
                "volume down", "decrease volume", "quieter",
                "mute", "silence", "quiet",
                
                # Application commands
                "close chrome", "close browser", "shut down chrome",
                "open settings", "preferences", "configuration",
                
                # Date commands
                "what's the date", "today's date", "current date",
                
                # Typing commands
                "type", "write", "input text",
            ],
            "intents": [
                # YouTube intents
                "open_youtube", "open_youtube", "open_youtube", "open_youtube",
                
                # Time intents
                "get_time", "get_time", "get_time", "get_time",
                
                # Search intents
                "open_google", "search", "search", "search",
                
                # Weather intents
                "weather", "weather", "weather", "weather",
                
                # Wikipedia intents
                "wikipedia", "wikipedia", "wikipedia", "wikipedia",
                
                # Conversation intents
                "talk", "talk", "talk", "conversation_mode",
                
                # System intents
                "screenshot", "screenshot", "screenshot", "screenshot",
                "open_file_manager", "open_file_manager", "open_file_manager", "open_file_manager",
                "system_info", "system_info", "system_info",
                "volume_up", "volume_up", "volume_up",
                "volume_down", "volume_down", "volume_down",
                "volume_mute", "volume_mute", "volume_mute",
                
                # Application intents
                "close_application", "close_application", "close_application",
                "open_settings", "open_settings", "open_settings",
                
                # Date intents
                "get_date", "get_date", "get_date",
                
                # Typing intents
                "type", "type", "type",
            ]
        }
    
    def fetch_commands_from_db(self):
        """Fetch commands with multiple fallback options"""
        try:
            # Try to import MongoDB first
            try:
                import pymongo
                return self._fetch_from_mongodb()
            except ImportError:
                logger.info("MongoDB not available, trying local file")
                
            # Try local JSON file
            if self.data_file.exists():
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    commands = data.get('commands', [])
                    intents = data.get('intents', [])
                    
                    if commands and intents:
                        logger.info("Loaded commands from local file")
                        return commands, intents
            
            # Use fallback data
            logger.info("Using fallback training data")
            return self.fallback_data['commands'], self.fallback_data['intents']
            
        except Exception as e:
            logger.error(f"Database fetch error: {e}")
            return self.fallback_data['commands'], self.fallback_data['intents']
    
    def _fetch_from_mongodb(self):
        """Fetch from MongoDB if available"""
        try:
            import pymongo
            client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
            
            # Test connection
            client.server_info()
            
            db = client['ai_assistant']
            collection = db['commands']
            
            commands_data = list(collection.find({}))
            
            if commands_data:
                commands = [item['command'] for item in commands_data]
                intents = [item['intent'] for item in commands_data]
                logger.info("Loaded commands from MongoDB")
                return commands, intents
            else:
                raise Exception("No data in MongoDB")
                
        except Exception as e:
            logger.warning(f"MongoDB connection failed: {e}")
            raise
    
    def save_commands_to_file(self, commands, intents):
        """Save commands to local JSON file"""
        try:
            data = {
                'commands': commands,
                'intents': intents,
                'updated': datetime.now().isoformat()
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info("Commands saved to local file")
            
        except Exception as e:
            logger.error(f"Failed to save commands: {e}")
