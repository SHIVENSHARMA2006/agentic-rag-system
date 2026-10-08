# Agentic RAG System

## LLM provider and API keys

Text generation uses Groq (`openai/gpt-oss-120b`) through Groq's OpenAI-compatible API. Add the key to the backend `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
LLM_MODEL=openai/gpt-oss-120b
```

Create a key in the [Groq Console](https://console.groq.com/keys). Keep the existing `GOOGLE_API_KEY` configured: Google is still used for document embeddings. Never commit `.env` or share API keys in chat.

## Chat conversations

`POST /chat` accepts a `question` and an optional `conversation_id` UUID. If no ID is supplied, the API generates one. The response includes the same `conversation_id`, an LLM-suggested `conversation_title`, `answer`, `sources`, and a safe `run` summary with step statuses and aggregate metrics. Raw warning text is not returned.

The backend keeps the latest eight successful user/assistant turns in process memory for each conversation. The query-understanding agent uses that history to rewrite follow-up questions as standalone retrieval queries; planning and response generation also receive recent turns. Memory expires after 24 hours of inactivity, is limited to 500 conversations, and is cleared when the backend process restarts. Use a shared persistent store such as Redis or a database before running multiple backend workers or deploying across instances.

Conversation IDs associate turns; they are not authentication or access-control tokens. Authentication is not currently implemented.
