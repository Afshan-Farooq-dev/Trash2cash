# TRASH2CASH Chatbot Integration Documentation

## Overview

The TRASH2CASH Smart Waste Management System now includes an AI-powered chatbot assistant that helps users navigate the dashboard and understand system features.

## Features

### 1. **Intelligent Assistance**

- Answers questions about dashboard features
- Explains waste disposal process
- Guides users to nearby bins
- Clarifies points and rewards system
- Troubleshoots common issues
- Provides hardware status information

### 2. **User Experience**

- **Floating Chat Icon**: Always accessible at bottom-right corner
- **Professional UI**: Clean, modern design matching system theme
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Responses**: Fast inference using Groq API
- **Conversation History**: Maintains context within session
- **Quick Actions**: Pre-defined questions for common queries

### 3. **Smart Restrictions**

- **Project-Specific**: Only answers questions about TRASH2CASH system
- **Professional Tone**: No jokes, emojis, or unrelated content
- **Concise Responses**: Under 150 words for clarity
- **Polite Redirects**: Guides users back to system topics if they stray

## Technical Implementation

### Backend Architecture

#### 1. **Groq API Integration** (`Light/chatbot.py`)

```python
- Uses Groq's LLaMA 3 8B model for fast inference
- System prompt ensures project-specific responses
- Conversation history management (last 10 exchanges)
- Error handling and fallback responses
```

#### 2. **API Endpoints**

```
POST /api/chatbot/message/
- Handles user messages
- Returns AI-generated responses
- Maintains conversation context

GET /api/chatbot/health/
- Checks chatbot availability
- Returns model information
```

#### 3. **Environment Configuration** (`.env`)

```dotenv
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama3-8b-8192
CHATBOT_MAX_HISTORY=10
```

### Frontend Components

#### 1. **Chat Widget** (`Light/templates/chatbot_widget.html`)

- **Floating Button**: Green gradient button with chat icon
- **Chat Container**: 380px × 550px modal window
- **Message Display**: User and bot messages with timestamps
- **Input Area**: Text input with send button
- **Typing Indicator**: Animated dots when AI is responding

#### 2. **Styling**

- Matches dashboard color scheme (#2F855A, #2B6CB0, #38B2AC)
- Professional gradient backgrounds
- Smooth animations and transitions
- Custom scrollbar styling
- Responsive breakpoints for mobile

#### 3. **JavaScript Features**

```javascript
- Toggle chatbot visibility
- Send messages via AJAX
- Handle quick action buttons
- Manage conversation history
- Auto-scroll to latest message
- Show/hide typing indicator
- Disable input during processing
```

## System Prompt

The chatbot uses a comprehensive system prompt that:

### Defines Role

```
"You are an AI assistant for the TRASH2CASH Smart Waste Management System."
```

### Sets Strict Rules

1. ONLY answer project-related questions
2. Be professional, concise, informative
3. NO jokes, NO emojis, NO unrelated topics
4. Redirect off-topic questions politely

### Lists Available Topics

- Dashboard navigation and statistics
- QR code scanning for waste disposal
- Finding nearby smart bins on map
- User profile and account management
- Points and rewards system
- Waste classification types
- Hardware status (ESP32 devices)
- Redemption process and history
- Issue reporting
- Notifications

### Provides Example Responses

Includes specific examples of how to answer common questions with proper format and detail level.

## Usage Instructions

### For Users

1. **Open Chat**: Click the green chat icon at bottom-right
2. **Ask Questions**: Type or use quick action buttons
3. **Get Answers**: Receive instant, relevant responses
4. **Continue Conversation**: Ask follow-up questions
5. **Close Chat**: Click X or chat button again

### For Developers

#### Installation Steps

1. **Install Groq SDK**:

```bash
pip install groq
```

2. **Configure Environment**:
   Add to `.env` file:

```dotenv
GROQ_API_KEY=your-groq-api-key-here
GROQ_MODEL=llama3-8b-8192
CHATBOT_MAX_HISTORY=10
```

3. **Update URLs**:
   Already added to `Light/urls.py`:

```python
path('api/chatbot/message/', chatbot.chatbot_message, name='chatbot_message'),
path('api/chatbot/health/', chatbot.chatbot_health, name='chatbot_health'),
```

4. **Include Widget**:
   Already included in `base.html`:

```django
{% include 'chatbot_widget.html' %}
```

#### Testing

1. **Check Availability**:

```bash
curl http://127.0.0.1:8000/api/chatbot/health/
```

2. **Test Message**:

```bash
curl -X POST http://127.0.0.1:8000/api/chatbot/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I dispose waste?"}'
```

#### Customization

**Modify System Prompt**:
Edit `SYSTEM_PROMPT` in `Light/chatbot.py` to add/remove topics or change response style.

**Adjust Styling**:
Modify CSS in `Light/templates/chatbot_widget.html` to match your design preferences.

**Change Model**:
Update `GROQ_MODEL` in `.env` to use different LLaMA models:

- `llama3-8b-8192` (default, fast)
- `llama3-70b-8192` (more capable, slower)
- `mixtral-8x7b-32768` (longer context)

## Example Conversations

### Example 1: Waste Disposal

**User**: "How do I dispose waste?"
**Bot**: "To dispose waste: 1) Go to the Dashboard and click 'Scan QR Code', 2) Scan the QR code on any smart bin, 3) The AI will classify your waste type, 4) Receive points based on the waste category. You can track your disposal history in the Waste History section."

### Example 2: Finding Bins

**User**: "Where are nearby bins?"
**Bot**: "To find nearby smart bins: Go to 'Find Nearby Bins' in the menu. The interactive map shows all available smart bins with their locations, capacity status, and distance from your current location. Green markers indicate bins with good capacity."

### Example 3: Points System

**User**: "How does the points system work?"
**Bot**: "You earn points for each waste disposal based on the type: Plastic (10 points), Metal (15 points), Glass (12 points), Paper and Cardboard (8 points each), General Trash (5 points). Points can be redeemed for rewards, bill payments, or charity donations in the Rewards Store."

### Example 4: Off-Topic Redirect

**User**: "Tell me a joke"
**Bot**: "I'm here to assist with the TRASH2CASH waste management system. I can help you with dashboard features, waste disposal, finding bins, or managing your profile. What would you like to know?"

## API Response Format

### Success Response

```json
{
  "success": true,
  "response": "AI-generated answer here...",
  "message_id": "unique_groq_message_id"
}
```

### Error Response

```json
{
  "error": "Error message here"
}
```

## Performance Considerations

### Response Time

- Average: 1-2 seconds
- Groq API is optimized for fast inference
- LLaMA 3 8B provides good balance of speed and quality

### Rate Limiting

- No built-in rate limiting currently
- Recommend adding per-user limits in production
- Example: 20 messages per minute per user

### Conversation History

- Stores last 10 exchanges per session
- History cleared when user closes browser
- Can be extended with database storage for persistence

## Security Considerations

1. **API Key Protection**:
   - Stored in `.env` file (not committed to Git)
   - Only accessible server-side
   - Never exposed to frontend

2. **Input Validation**:
   - Message length validation
   - Sanitization of user input
   - XSS protection via Django's built-in security

3. **CSRF Protection**:
   - Disabled for API endpoint
   - Could be re-enabled with proper token handling

## Future Enhancements

### Potential Features

1. **Persistent History**: Store conversations in database
2. **User Context**: Access user's actual data (points, history)
3. **Multilingual Support**: Support multiple languages
4. **Voice Input**: Speech-to-text integration
5. **Analytics**: Track common questions and improve responses
6. **Admin Dashboard**: View chatbot usage statistics

### Model Improvements

1. **Fine-tuning**: Train on actual user queries
2. **RAG Integration**: Use vector database for accurate information retrieval
3. **Function Calling**: Direct integration with system actions

## Troubleshooting

### Chatbot Not Appearing

- Check that `chatbot_widget.html` is included in `base.html`
- Verify Font Awesome is loaded
- Check browser console for JavaScript errors

### API Errors

- Verify `GROQ_API_KEY` is set in `.env`
- Check Groq API status and quotas
- Review Django logs for detailed error messages

### Slow Responses

- Consider using faster model (llama3-8b-8192)
- Check network connectivity
- Monitor Groq API performance

### Incorrect Answers

- Review and update `SYSTEM_PROMPT`
- Add more specific examples
- Consider switching to larger model

## Support

For issues or questions:

1. Check Django server logs
2. Review browser console
3. Test API endpoints directly
4. Verify environment configuration
5. Check Groq API documentation: https://console.groq.com/docs

---

**Version**: 1.0
**Last Updated**: January 27, 2026
**Powered by**: Groq AI (LLaMA 3 8B)
