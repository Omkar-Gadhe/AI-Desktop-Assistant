# router_logic.py
import action as action_engine
from services.nlp_service import nlp_service

act_words = ("launch", "open", "run", "start")
exit_cmd = ("bye", "exit", "close", "goodbye")

def router(user_input: str):
    '''Smart grammatical router leveraging tokenization and phrase matching.'''
    text = user_input.lower().strip()

    # 1. Global Exit Check
    if any(word in text for word in exit_cmd):
        return {"intent": "exit", "action_word": None, "matched_apps": []}

    # 2. Grab the pre-warmed, memory-resident spaCy objects from your service container
    nlp = nlp_service.nlp
    matcher = nlp_service.matcher
    
    # 3. Process the sentence linguistically (ONCE)
    doc = nlp(user_input)
    
    # 4. Extract the command verb only if its grammatical role is an actual VERB
    action_verb = None
    for token in doc:
        if token.text.lower() in act_words and token.pos_ == "VERB":
            action_verb = token.text.lower()
            break  

    # 5. Extract unique matching apps based on strict token boundaries
    matches = matcher(doc)
    matched_apps = list({doc[start:end].text.lower() for match_id, start, end in matches})

    # 6. Intent Assignment
    if action_verb and matched_apps:
        intent = "action"
    else:
        intent = "chat"

    return {
        "intent": intent,
        "action_word": action_verb,
        "matched_apps": matched_apps
    }