# history.py
from google.genai import types

class ShortTermMemory:
    def __init__(self, max_turns=5):
        # 1 turn = 1 user prompt + 1 model response (2 messages total)
        self.max_messages = max_turns * 2
        self.history = []

    def add_message(self, role: str, text: str):
        """Formats and logs a dialogue turn using the modern Google SDK Schema."""
        # Convert raw strings into the official structured object Google expects
        content_object = types.Content(
            role=role,
            parts=[types.Part.from_text(text=text)]
        )
        self.history.append(content_object)
        
        # Sliding Window Trim: Automatically chop off the oldest history 
        # when we exceed our token-saving budget ceiling.
        if len(self.history) > self.max_messages:
            self.history = self.history[-self.max_messages:]

    def get_context(self):
        """Returns the managed context list to be sent to the API."""
        return self.history