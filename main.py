# chatbot.py
import time
import ai_gateway
import action

from history import ShortTermMemory  # 1. Import your new memory module

# 2. Instantiate memory once at startup so it stays alive across prompts
# Initialize memory once at application startup
chat_memory = ShortTermMemory(max_turns=3)

# Global Control Settings
ACT_WORDS = ("launch", "open", "run", "start")
EXIT_COMMANDS = ("bye", "exit", "close", "goodbye")


def parse_user_input(user_input: str):
    """JOB 1: String Parsing. 
    Inspects the prompt, identifies special flags, and returns clean data.
    """
    is_hard_task = False
    clean_prompt = user_input
    
    if user_input.lower().startswith("/think"):
        is_hard_task = True
        clean_prompt = user_input[6:].strip()
        
    return clean_prompt, is_hard_task


def stream_and_print_response(context_history, is_hard_task: bool) -> str:
    """JOB 2: Stream Consumption.
    Loops through network chunks, prints them in real time, and harvests them into a string.
    """
    print("AI: ", end="", flush=True)
    full_ai_response = ""
    
    # Call the network gateway pipeline
    chunks = ai_gateway.generate_response_stream(context_history, use_thinking_model=is_hard_task)
    
    for chunk in chunks:
        print(chunk, end="", flush=True)
        full_ai_response += chunk
        
    print()  # Print a clean newline when the stream completes successfully
    return full_ai_response


def execute_network_with_retry(context_history, is_hard_task: bool) -> str:
    """JOB 3: Reliability & Resilience.
    Orchestrates network retries and exponential backoff timing if Google drops the ball.
    """
    max_retries = 3
    retry_delay = 2 
    
    for attempt in range(max_retries):
        try:
            # Delegate the actual streaming work to our stream worker
            return stream_and_print_response(context_history, is_hard_task)
            
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"\n\n[System Error: Google's servers are completely overloaded. Try again soon.]\n")
                raise e  # Bubble the exception up if we are completely out of retries
            else:
                print(f"\n[Server busy... retrying in {retry_delay}s (Attempt {attempt + 1}/{max_retries})...]")
                time.sleep(retry_delay)
                retry_delay *= 2
    return ""


def chat_brain(user_input: str):
    """JOB 4: High-Level Orchestrator.
    Does no core computational work itself. It simply dictates the operational workflow line-by-line.
    """
    if not user_input:
        return
        
    # 1. Parse incoming strings cleanly
    clean_prompt, is_hard_task = parse_user_input(user_input)
    
    # 2. Record the question to memory
    chat_memory.add_message(role="user", text=clean_prompt)
    
    # 3. Fire the network pipeline safely and fetch the generated text
    try:
        current_context = chat_memory.get_context()
        final_response = execute_network_with_retry(current_context, is_hard_task)
        
        # 4. If the call was successful, record the answer to memory
        if final_response:
            chat_memory.add_message(role="model", text=final_response)
            
    except Exception:
        # Prevent the whole loop from crashing if the retry engine ultimately failed
        pass


def detect_intent(text):
    text = text.lower()
    # Cleaner lookup using your global control variables!
    if any(word in text for word in ACT_WORDS):
        return "launch_app"
    if any(word in text for word in EXIT_COMMANDS):
        return "exit"
    return "chat"


if __name__ == "__main__":
    # Print the setup menu ONCE at the absolute start of the program
    print("==================================================")
    print("Chatbot initialized! (Streaming + Smart Routing Active)")
    print("-> Type normally for the FAST model.")
    print("-> Type '/think' first for the DEEP THINKING model.")
    print("==================================================")

    while True:
        # FIXED: Removed .lower() from here so the AI gets clean data
        user_input = input("\nYou: ").strip()
        
        if not user_input:
            print("Please type something.")
            continue
    
        intent = detect_intent(user_input)
    
        if intent == "launch_app":
            action.act_brain(user_input)
        elif intent == "exit":
            print("Good Bye Ghost!")
            break
        else:
            chat_brain(user_input)