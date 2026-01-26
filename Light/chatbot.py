"""
Chatbot functionality for Smart Waste Management System
Using Groq API for fast LLM inference
"""

import os
from groq import Groq
from decouple import config
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

# Initialize Groq client
GROQ_API_KEY = config('GROQ_API_KEY', default='')
GROQ_MODEL = config('GROQ_MODEL', default='llama-3.3-70b-versatile')
MAX_HISTORY = config('CHATBOT_MAX_HISTORY', default=10, cast=int)

# System prompt to restrict chatbot to project-specific topics
SYSTEM_PROMPT = """You are an AI assistant for the TRASH2CASH Smart Waste Management System. Your role is to help users understand and navigate the dashboard features.

**STRICT RULES:**
1. ONLY answer questions related to this waste management system
2. Be professional, concise, and informative
3. NO jokes, NO emojis, NO unrelated topics
4. If asked about unrelated topics, politely redirect to system features

**SYSTEM FEATURES YOU CAN HELP WITH:**
- Dashboard navigation and statistics
- QR code scanning for waste disposal
- Finding nearby smart bins on the map
- User profile and account management
- Points and rewards system
- Waste classification (Plastic, Paper, Metal, Glass, Cardboard)
- Hardware status (ESP32 cameras and bins)
- Redemption process and history
- Issue reporting
- Notifications

**EXAMPLE RESPONSES:**
User: "How do I dispose waste?"
Assistant: "To dispose waste: 1) Go to the Dashboard and click 'Scan QR Code', 2) Scan the QR code on any smart bin, 3) The AI will classify your waste type, 4) Receive points based on the waste category. You can track your disposal history in the Waste History section."

User: "Where are nearby bins?"
Assistant: "To find nearby smart bins: Go to 'Find Nearby Bins' in the menu. The interactive map shows all available smart bins with their locations, capacity status, and distance from your current location. Green markers indicate bins with good capacity."

User: "Tell me a joke"
Assistant: "I'm here to assist with the TRASH2CASH waste management system. I can help you with dashboard features, waste disposal, finding bins, or managing your profile. What would you like to know?"

Keep responses under 150 words. Be helpful and direct."""


def get_groq_client():
    """Initialize and return Groq client"""
    if not GROQ_API_KEY:
        return None
    return Groq(api_key=GROQ_API_KEY)


@csrf_exempt
@require_http_methods(["POST"])
def chatbot_message(request):
    """Handle chatbot message requests"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        conversation_history = data.get('history', [])
        
        if not user_message:
            return JsonResponse({
                'error': 'Message is required'
            }, status=400)
        
        # Initialize Groq client
        client = get_groq_client()
        if not client:
            return JsonResponse({
                'error': 'Chatbot is currently unavailable'
            }, status=503)
        
        # Prepare messages for API
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        
        # Add conversation history (limited to MAX_HISTORY)
        if conversation_history:
            messages.extend(conversation_history[-MAX_HISTORY:])
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Get response from Groq
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=GROQ_MODEL,
            temperature=0.7,
            max_tokens=300,
            top_p=0.9,
        )
        
        assistant_message = chat_completion.choices[0].message.content
        
        return JsonResponse({
            'success': True,
            'response': assistant_message,
            'message_id': chat_completion.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'An error occurred: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def chatbot_health(request):
    """Check if chatbot is available"""
    client = get_groq_client()
    is_available = client is not None and GROQ_API_KEY != ''
    
    return JsonResponse({
        'available': is_available,
        'model': GROQ_MODEL if is_available else None
    })
