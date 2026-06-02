# ai_gateway.py
from google import genai
from google.genai import types 
import config

# The new unified Google client automatically finds your GEMINI_API_KEY from the environment variables!
client = genai.Client()

# 1. Define a strict, voice-friendly personality for everyday tasks
FAST_ASSISTANT_PERSONALITY = (
    "You are a concise, sharp, and voice-optimized desktop assistant. "
    "Keep your answers short, direct, and strictly under 3 sentences or lesser. "
    "Never use bullet points, markdown tables, or heavy symbols, as your "
    "responses will be read aloud by a text-to-speech engine. Be conversational."
)

def generate_response_stream(history_list, use_thinking_model=False):
    # 1. Select the appropriate model
    selected_model = config.MODEL_THINKING if use_thinking_model else config.MODEL_FAST
    
    # 2. Configure the thinking behavior dynamically
    if use_thinking_model:
        # Allow a token budget for complex reasoning tasks
        api_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=2048) 
        )
    else:
        # 2. Apply the personality constraint ONLY to the fast model
        api_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            system_instruction=FAST_ASSISTANT_PERSONALITY  # <--- The Magic Constraint
        )
    # Use the new models streaming method
    response = client.models.generate_content_stream(
        model=selected_model,
        contents=history_list,
        config=api_config  # <--- Added configuration object
    )
    
    for chunk in response:
        try:
            if chunk.text:
                yield chunk.text
        except (ValueError, AttributeError):
            # Keeps our safe protective shield intact if a chunk is empty
            continue