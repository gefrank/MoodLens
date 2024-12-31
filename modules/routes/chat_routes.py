from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from modules.services.emotional_chatbot import EmotionalChatbot
from modules.models import AppConfig

chat_routes = Blueprint('chat', __name__)

@chat_routes.route("/")
@login_required
def chat_interface():
    """Render the chat interface"""
    # Fetch the current AI model from AppConfig
    config = AppConfig.query.filter_by(key="ai_model").first()
    current_model = "OpenAI" if config and config.value == "openai" else "DistilBERT"
    return render_template("chat.html", current_model=current_model)


@chat_routes.route("/send", methods=["POST"])
@login_required
def send_message():
    """Handle sending a message to the chatbot"""
    message = request.json.get("message", "").strip()
    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    try:
        # Initialize chatbot with current user's ID
        chatbot = EmotionalChatbot(current_user.id)
        response, metadata = chatbot.process_message(message)
        
        # Add debug logging
        print(f"Message: {message}")
        print(f"Response: {response}")
        print(f"Metadata: {metadata}")
        
        return jsonify({
            "response": response,
            "sentiment": metadata.get("sentiment", "NEUTRAL"),
            "confidence": metadata.get("confidence", 0.5)
        })
        
    except Exception as e:
        # Add error logging
        print(f"Error in send_message: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
    

@chat_routes.route("/history")
@login_required
def get_history():
    """Get chat history for the current session"""
    try:
        chatbot = EmotionalChatbot(current_user.id)
        history = EmotionalChatbot.get_chat_history(chatbot.session_id)
        return jsonify({"history": history})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500