#...File name initialized
# chatbot.py

#...Imported all necessary modules
import time
import ai_gateway
import action as action_engine
from history import ShortTermMemory  
from ass_log import logger
import router as rl
from services.nlp_service import nlp_service

#...Instantiate memory once at startup so it stays alive across prompts
chat_memory = ShortTermMemory(max_turns=5)

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
    Loops through network chunks, prints them in real time, and builds the string cleanly.
    """
    print("AI: ", end="", flush=True)
    response_chunks = []  # OPTIMIZED: Dynamic array allocation instead of immutable strings
    
    # Call the network gateway pipeline
    chunks = ai_gateway.generate_response_stream(context_history, use_thinking_model=is_hard_task)
    
    for chunk in chunks:
        print(chunk, end="", flush=True)
        response_chunks.append(chunk)
        
    print()  # Print a clean newline when the stream completes successfully
    
    # Perform a single, linear-time C-level memory joint pass
    return "".join(response_chunks)

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
                # ─── LOG CRITICAL API FAILURE ───
                logger.error(f"Gemini API completely failed after {max_retries} attempts. Error: {str(e)}")
                raise # Bubble the exception up if we are completely out of retries
            else:
                print(f"\n[Server busy... retrying in {retry_delay}s (Attempt {attempt + 1}/{max_retries})...]")
                # ─── LOG THE RETRY ATTEMPT ───
                logger.warning(f"API 503 Server Busy. Retrying in {retry_delay}s. (Attempt {attempt + 1}/{max_retries})")
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
            # ─── LOG A SUCCESSFUL ACTION ───
            logger.info(f"Successfully saved chatbot's history!")
            
    except Exception as e:
        # FIXED: Capture the exact instance 'e' and trigger a full traceback dump
        logger.error(
            f"The core engine encountered an unexpected failure: {str(e)}", 
            exc_info=True
        )
        
        # Give the user a clear, professional warning without spilling raw Python errors on screen
        print("\n[Notice: A temporary internal engine error occurred. The system safely recovered.]")

if __name__ == "__main__":
    print("==================================================")
    # Trigger the heavy lifting explicitly during app startup
    nlp_service.initialize(app_registry=action_engine.APPS)
    print("Chatbot initialized! (Streaming + Smart Routing Active)")
    print("-> Type normally for the FAST model.")
    print("-> Type '/think' first for the DEEP THINKING model.")
    print("==================================================")
    # Print the setup menu ONCE at the absolute start of the program

    while True:
        # FIXED: Removed .lower() from here so the AI gets clean data
        user_input = input("\nYou: ")
        
        if not user_input:
            print("Please type something.")
            continue
    
        result = rl.router(user_input)
    
        # Look how clean these dictionary checks are now!
        if result["intent"] == "action":
            # Extract the app name the router ALREADY found
            # 1. The router did 100% of the extraction heavy lifting
            primary_app = result["matched_apps"][0]
            
            # Pass BOTH the raw text and the pre-discovered app name# 2. The action engine does 100% execution—no text parsing allowed!
            action_engine.act_brain(primary_app)
            
        elif result["intent"] == "exit":
            print("Good Bye Ghost!")
            break
        else:
            chat_brain(user_input)