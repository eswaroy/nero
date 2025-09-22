from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, classification_report
import joblib
import logging
import numpy as np
from pathlib import Path
from config import Config

logger = logging.getLogger(__name__)

class IntentClassifier:
    def __init__(self):
        self.config = Config()
        self.model = None
        self.is_trained = False
        
    def train_model(self, commands, intents):
        """Train the intent classification model"""
        try:
            if len(commands) < 10:  # Need minimum data
                logger.warning("Insufficient training data, using fallback model")
                return self._create_fallback_model()
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                commands, intents, 
                test_size=0.2, 
                random_state=42,
                stratify=intents
            )
            
            # Create pipeline with optimized parameters
            self.model = make_pipeline(
                TfidfVectorizer(
                    max_features=1000,
                    ngram_range=(1, 2),
                    stop_words='english'
                ),
                MultinomialNB(alpha=0.1)
            )
            
            # Train model
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            logger.info(f"Model trained with accuracy: {accuracy:.2f}")
            
            # Save model
            model_path = self.config.model_file
            joblib.dump(self.model, model_path)
            self.is_trained = True
            
            return self.model
            
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            return self._create_fallback_model()
    
    def _create_fallback_model(self):
        """Create a simple fallback model with basic intents"""
        basic_commands = [
            "open youtube", "play music", "youtube",
            "what time is it", "current time", "time",
            "open google", "search google", "google",
            "what's the weather", "weather forecast", "weather",
            "tell me about", "wikipedia", "search wikipedia",
            "talk to me", "let's chat", "conversation",
            "take screenshot", "capture screen", "screenshot",
            "open file manager", "show files", "explorer",
            "system information", "computer stats", "system info","start live talk", "live conversation", "live chat", "talk live",
            "get news", "latest news", "current news", "news today",
            "research", "analyze", "deep dive", "investigate",
            "ask ai", "chat with ai", "ai conversation", "smart chat"
        ]
        
        basic_intents = [
            "open_youtube", "open_youtube", "open_youtube",
            "get_time", "get_time", "get_time",
            "open_google", "search", "open_google",
            "weather", "weather", "weather",
            "wikipedia", "wikipedia", "wikipedia",
            "talk", "talk", "conversation_mode",
            "screenshot", "screenshot", "screenshot",
            "open_file_manager", "open_file_manager", "open_file_manager",
            "system_info", "system_info", "system_info","start_live_talk", "start_live_talk", "start_live_talk", "start_live_talk",
            "get_news", "get_news", "get_news", "get_news", 
            "research", "research", "research", "research",
            "ai_chat", "ai_chat", "ai_chat", "ai_chat"
        ]
        
        self.model = make_pipeline(
            TfidfVectorizer(ngram_range=(1, 2)),
            MultinomialNB()
        )
        
        self.model.fit(basic_commands, basic_intents)
        self.is_trained = True
        
        logger.info("Fallback model created")
        return self.model
    
    def load_model(self):
        """Load existing model"""
        try:
            model_path = self.config.model_file
            if model_path.exists():
                self.model = joblib.load(model_path)
                self.is_trained = True
                logger.info("Model loaded successfully")
                return self.model
            else:
                logger.warning("No saved model found")
                return None
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return None
    
    def classify_intent(self, command):
        """Classify intent with confidence scoring"""
        try:
            if not self.is_trained:
                return "unknown"
            
            # Get prediction with probability
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba([command])[0]
                classes = self.model.classes_
                
                # Get highest confidence prediction
                max_prob_idx = np.argmax(probabilities)
                confidence = probabilities[max_prob_idx]
                predicted_intent = classes[max_prob_idx]
                
                # If confidence is too low, treat as conversational
                if confidence < 0.3:
                    return "talk"
                
                logger.debug(f"Intent: {predicted_intent}, Confidence: {confidence:.2f}")
                return predicted_intent
            else:
                return self.model.predict([command])[0]
                
        except Exception as e:
            logger.error(f"Intent classification failed: {e}")
            return "talk"  # Fallback to conversation
    
    def add_training_data(self, command, intent):
        """Add new training data (for online learning)"""
        # This could be implemented for continuous learning
        pass
