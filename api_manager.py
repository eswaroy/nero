import openai
import asyncio
import websockets
import json
import logging
import threading
import queue
import base64
from typing import Optional, Dict, Any, List
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class PerplexityManager:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )
        
    def search_and_chat(self, query: str, conversation_history: List[Dict] = None) -> str:
        """Enhanced search with conversation context"""
        try:
            messages = []
            
            # Add conversation history for context
            if conversation_history:
                messages.extend(conversation_history[-5:])  # Last 5 messages for context
            
            # Add current query
            messages.append({
                "role": "user",
                "content": f"Please provide a comprehensive answer about: {query}"
            })
            
            response = self.client.chat.completions.create(
                model="llama-3.1-sonar-large-128k-online",
                messages=messages,
                temperature=0.2,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Perplexity API error: {e}")
            return f"I encountered an error while searching for information: {str(e)}"
    
    def get_latest_news(self, topic: str = None) -> str:
        """Get latest news on a topic"""
        try:
            query = f"Latest news about {topic}" if topic else "Latest news today"
            
            response = self.client.chat.completions.create(
                model="llama-3.1-sonar-large-128k-online",
                messages=[{
                    "role": "user", 
                    "content": f"Give me the top 5 latest news stories about {query}. Include dates and sources."
                }],
                temperature=0.1,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Unable to fetch news: {str(e)}"
    
    def analyze_and_research(self, query: str) -> str:
        """Deep research and analysis"""
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-sonar-large-128k-online",
                messages=[{
                    "role": "system",
                    "content": "You are a research assistant. Provide detailed, well-researched answers with current information and multiple perspectives."
                }, {
                    "role": "user",
                    "content": query
                }],
                temperature=0.3,
                max_tokens=3000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Research error: {str(e)}"

class GeminiLiveManager:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.websocket = None
        self.session_active = False
        self.audio_queue = queue.Queue()
        self.response_queue = queue.Queue()
        self.conversation_history = []
        
    async def start_live_session(self):
        """Start Gemini Live WebSocket session"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # WebSocket URL for Gemini Live API
            ws_url = "wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService/BidiGenerateContent"
            
            self.websocket = await websockets.connect(ws_url, extra_headers=headers)
            self.session_active = True
            
            # Send initial configuration
            config = {
                "setup": {
                    "model": "models/gemini-2.0-flash-live-001",
                    "generation_config": {
                        "response_modalities": ["AUDIO", "TEXT"],
                        "speech_config": {
                            "voice_config": {
                                "prebuilt_voice_config": {
                                    "voice_name": "Aoede"
                                }
                            }
                        }
                    }
                }
            }
            
            await self.websocket.send(json.dumps(config))
            logger.info("Gemini Live session started")
            
            # Start listening for responses
            asyncio.create_task(self._listen_for_responses())
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start Gemini Live session: {e}")
            return False
    
    async def send_text_message(self, text: str):
        """Send text message to Gemini Live"""
        try:
            if not self.session_active or not self.websocket:
                return False
                
            message = {
                "client_content": {
                    "turns": [{
                        "role": "user",
                        "parts": [{
                            "text": text
                        }]
                    }],
                    "turn_complete": True
                }
            }
            
            await self.websocket.send(json.dumps(message))
            self.conversation_history.append({"role": "user", "content": text})
            return True
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    async def send_audio_chunk(self, audio_data: bytes):
        """Send audio chunk to Gemini Live"""
        try:
            if not self.session_active or not self.websocket:
                return False
                
            # Convert audio to base64
            audio_b64 = base64.b64encode(audio_data).decode('utf-8')
            
            message = {
                "realtime_input": {
                    "media_chunks": [{
                        "mime_type": "audio/pcm",
                        "data": audio_b64
                    }]
                }
            }
            
            await self.websocket.send(json.dumps(message))
            return True
            
        except Exception as e:
            logger.error(f"Error sending audio: {e}")
            return False
    
    async def _listen_for_responses(self):
        """Listen for responses from Gemini Live"""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                
                # Handle text responses
                if "server_content" in data:
                    content = data["server_content"]
                    if "model_turn" in content:
                        for part in content["model_turn"]["parts"]:
                            if "text" in part:
                                text_response = part["text"]
                                self.response_queue.put({"type": "text", "content": text_response})
                                self.conversation_history.append({"role": "assistant", "content": text_response})
                
                # Handle audio responses
                if "server_content" in data and "model_turn" in data["server_content"]:
                    for part in data["server_content"]["model_turn"]["parts"]:
                        if "inline_data" in part:
                            audio_data = base64.b64decode(part["inline_data"]["data"])
                            self.response_queue.put({"type": "audio", "content": audio_data})
                
        except Exception as e:
            logger.error(f"Error in live response listener: {e}")
    
    def get_response(self, timeout: float = 5.0) -> Optional[Dict]:
        """Get response from queue"""
        try:
            return self.response_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    async def end_session(self):
        """End Gemini Live session"""
        try:
            self.session_active = False
            if self.websocket:
                await self.websocket.close()
            logger.info("Gemini Live session ended")
        except Exception as e:
            logger.error(f"Error ending session: {e}")

class EnhancedAPIManager:
    def __init__(self, perplexity_key: str, gemini_key: str):
        self.perplexity = PerplexityManager(perplexity_key)
        self.gemini_live = GeminiLiveManager(gemini_key)
        self.conversation_context = []
        self.live_mode_active = False
        
    def smart_query_router(self, query: str) -> tuple[str, str]:
        """Intelligently route queries to appropriate API"""
        query_lower = query.lower()
        
        # Real-time/current information keywords
        current_info_keywords = ['news', 'latest', 'current', 'today', 'recent', 'now', 'weather', 'stock', 'price']
        
        # Conversational keywords
        conversation_keywords = ['chat', 'talk', 'discuss', 'conversation', 'tell me', 'what do you think']
        
        # Research keywords
        research_keywords = ['analyze', 'research', 'compare', 'explain', 'deep dive', 'comprehensive']
        
        if any(keyword in query_lower for keyword in current_info_keywords):
            return "perplexity_news", query
        elif any(keyword in query_lower for keyword in research_keywords):
            return "perplexity_research", query
        elif any(keyword in query_lower for keyword in conversation_keywords):
            return "gemini_live", query
        else:
            # Default to Perplexity for general queries
            return "perplexity_search", query
    
    def process_query(self, query: str) -> str:
        """Process query through appropriate API"""
        try:
            route, processed_query = self.smart_query_router(query)
            
            if route == "perplexity_news":
                return self.perplexity.get_latest_news(processed_query)
            elif route == "perplexity_research":
                return self.perplexity.analyze_and_research(processed_query)
            elif route == "perplexity_search":
                return self.perplexity.search_and_chat(processed_query, self.conversation_context)
            elif route == "gemini_live":
                # For now, use text-based Gemini API
                return self._gemini_text_chat(processed_query)
            
        except Exception as e:
            logger.error(f"Query processing error: {e}")
            return f"I encountered an error processing your query: {str(e)}"
    
    def _gemini_text_chat(self, query: str) -> str:
        """Fallback Gemini text chat"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.gemini_live.api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            # Add conversation context
            full_prompt = query
            if self.conversation_context:
                context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.conversation_context[-3:]])
                full_prompt = f"Previous context:\n{context}\n\nCurrent question: {query}"
            
            response = model.generate_content(full_prompt)
            
            # Update conversation context
            self.conversation_context.append({"role": "user", "content": query})
            self.conversation_context.append({"role": "assistant", "content": response.text})
            
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini text chat error: {e}")
            return f"Gemini chat error: {str(e)}"
    
    async def start_live_conversation(self):
        """Start live conversation mode"""
        try:
            success = await self.gemini_live.start_live_session()
            if success:
                self.live_mode_active = True
                return "Live conversation mode activated! You can now talk naturally."
            else:
                return "Failed to start live conversation mode."
        except Exception as e:
            return f"Error starting live mode: {str(e)}"
    
    async def end_live_conversation(self):
        """End live conversation mode"""
        try:
            await self.gemini_live.end_session()
            self.live_mode_active = False
            return "Live conversation mode ended."
        except Exception as e:
            return f"Error ending live mode: {str(e)}"
