from datetime import datetime
from typing import Dict, Tuple, Optional, List
import random
from modules.services.sentiment_service import analyze_sentiment
from modules.utilities.database import db
from modules.models import ChatSession, ChatMessage, User
import openai

class EmotionalChatbot:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self._ensure_active_session()
        
        # Enhanced response templates with more variety
        self.response_templates = {
            "POSITIVE": [
                "I'm glad you're feeling positive! {response}",
                "That's wonderful! {response}",
                "Your enthusiasm is contagious! {response}",
                "It's great to hear you're in good spirits! {response}",
                "That's really positive news! {response}"
            ],
            "NEGATIVE": [
                "I understand this might be difficult. {response}",
                "I'm here to listen and support you. {response}",
                "Let's work through this together. {response}",
                "I hear your concerns. {response}",
                "That sounds challenging. {response}"
            ],
            "NEUTRAL": [
                "{response}",
                "I understand. {response}",
                "I see what you mean. {response}",
                "That's interesting. {response}",
                "Thank you for sharing that. {response}"
            ]
        }
        
        # Conversation state tracking
        self.conversation_state = {
            "consecutive_emotions": [],
            "topics_discussed": set(),
            "message_count": 0
        }

    def _ensure_active_session(self) -> None:
        """Create a new chat session if none exists for the user"""
        session = ChatSession.query.filter_by(
            user_id=self.user_id
        ).order_by(ChatSession.last_interaction.desc()).first()
        
        # Create new session if none exists or last one is old
        time_diff = datetime.now() - session.last_interaction if session else None
        if not session or (time_diff and time_diff.total_seconds() > 3600):
            session = ChatSession(user_id=self.user_id)
            db.session.add(session)
            db.session.commit()
        
        self.session_id = session.id

    def _get_recent_emotions(self, limit: int = 5) -> List[str]:
        """Get the most recent emotions with increased history"""
        recent_messages = ChatMessage.query.filter_by(
            session_id=self.session_id
        ).order_by(ChatMessage.timestamp.desc()).limit(limit).all()
        
        return [msg.sentiment for msg in recent_messages if msg.sentiment]

    def _analyze_conversation_context(self, sentiment: str) -> Dict:
        """Analyze conversation context for better response generation"""
        # Update emotion tracking
        self.conversation_state["consecutive_emotions"].append(sentiment)
        if len(self.conversation_state["consecutive_emotions"]) > 5:
            self.conversation_state["consecutive_emotions"].pop(0)
            
        # Analyze emotional patterns
        emotional_pattern = {
            "consistent_emotion": len(set(self.conversation_state["consecutive_emotions"][-3:])) == 1,
            "emotion_shift": len(self.conversation_state["consecutive_emotions"]) >= 2 and
                           self.conversation_state["consecutive_emotions"][-1] != 
                           self.conversation_state["consecutive_emotions"][-2],
            "persistent_negative": all(emotion == "NEGATIVE" for emotion in 
                                    self.conversation_state["consecutive_emotions"][-3:])
        }
        
        return emotional_pattern

    def _generate_contextual_response(self, base_response: str, context: Dict) -> str:
        """Generate response with contextual awareness"""
        response = base_response
        
        # Add contextual elements based on conversation analysis
        if context.get("persistent_negative"):
            response = "I notice you've been feeling down for a while. " + response
            response += " Remember, I'm here to support you, and it's okay to take time to process your feelings."
        elif context.get("emotion_shift"):
            response = "I notice a change in your emotional tone. " + response
        elif context.get("consistent_emotion") and self.conversation_state["message_count"] > 3:
            response += " Would you like to explore this further?"
            
        return response

    def process_message(self, user_input: str) -> Tuple[str, Dict]:
        """Process a user message with enhanced context awareness"""
        try:
            # Update message counter
            self.conversation_state["message_count"] += 1
            
            # Analyze sentiment
            sentiment, confidence = analyze_sentiment(user_input)
            
            # Get conversation context
            context = self._analyze_conversation_context(sentiment)
            
            # Log user message
            user_message = ChatMessage(
                session_id=self.session_id,
                message_type='user',
                content=user_input,
                sentiment=sentiment,
                confidence=confidence
            )
            db.session.add(user_message)
            
            # Generate base response
            base_response = self._generate_response(user_input, sentiment)
            
            # Add context-aware elements
            final_response = self._generate_contextual_response(base_response, context)
            
            # Log bot response
            bot_message = ChatMessage(
                session_id=self.session_id,
                message_type='bot',
                content=final_response
            )
            db.session.add(bot_message)
            
            # Update session
            session = ChatSession.query.get(self.session_id)
            session.last_interaction = datetime.now()
            db.session.commit()
            
            return final_response, {
                'sentiment': sentiment,
                'confidence': float(confidence)
            }
            
        except Exception as e:
            print(f"Error in process_message: {str(e)}")
            import traceback
            print(traceback.format_exc())
            raise

    def _generate_response(self, user_input: str, sentiment: str) -> str:
        """Generate an emotionally intelligent response with topic awareness"""
        # Enhanced topic detection
        topics = {
            "greeting": ['hello', 'hi', 'hey', 'morning', 'afternoon', 'evening'],
            "farewell": ['bye', 'goodbye', 'later', 'night', 'see you'],
            "gratitude": ['thanks', 'thank you', 'appreciate'],
            "problem": ['help', 'issue', 'problem', 'trouble', 'worried'],
            "emotion": ['feel', 'feeling', 'felt', 'happy', 'sad', 'angry']
        }
        
        # Detect topics
        current_topics = set()
        user_input_lower = user_input.lower()
        for topic, keywords in topics.items():
            if any(keyword in user_input_lower for keyword in keywords):
                current_topics.add(topic)
                self.conversation_state["topics_discussed"].add(topic)
        
        # Generate appropriate response based on topics and sentiment
        if "greeting" in current_topics:
            base_response = random.choice([
                "Welcome back! How are you feeling today?",
                "Hello! It's great to see you again.",
                "Hi there! I'm here to chat and help if needed."
            ])
        elif "farewell" in current_topics:
            base_response = random.choice([
                "Take care! Remember, I'm here whenever you need to talk.",
                "Goodbye for now! Looking forward to our next conversation.",
                "Have a great time! Come back anytime you want to chat."
            ])
        elif "gratitude" in current_topics:
            base_response = random.choice([
                "You're welcome! I'm glad I could help.",
                "It's my pleasure to assist you!",
                "I'm here to help anytime you need it."
            ])
        elif "problem" in current_topics:
            base_response = random.choice([
                "Let's work on this together. Can you tell me more?",
                "I'm here to help you work through this.",
                "Would you like to explore possible solutions together?"
            ])
        else:
            base_response = random.choice([
                "I understand how you feel.",
                "Thank you for sharing that with me.",
                "Let's explore that further."
            ])
        
        # Apply emotional template
        template = random.choice(self.response_templates.get(sentiment, self.response_templates["NEUTRAL"]))
        return template.format(response=base_response)

    @staticmethod
    def get_chat_history(session_id: int) -> list:
        """Get the chat history for a session with emotion metadata"""
        messages = ChatMessage.query.filter_by(
            session_id=session_id
        ).order_by(ChatMessage.timestamp).all()
        
        return [{
            'type': msg.message_type,
            'content': msg.content,
            'sentiment': msg.sentiment,
            'confidence': msg.confidence,
            'timestamp': msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        } for msg in messages]