import subprocess
import os

print("Welcome Ghost")

act_words = ("launch", "open", "run")
apps = {
    "firefox": "firefox",
    "vs code": "code"
}
responses = {
        "hi": "Nihao,",
        "how are you": "I'm fine\nHow about you?",
        "who are you": "Your Assistant\nHow can I help you?"
    }
exit_commands = ("bye","exit","close","goodbye")
def chat_brain(user_input):

    if user_input in responses:
        print(responses[user_input])

    elif "good morning" in user_input:
        print("Good Morning Ghost!")

    elif "beautiful" in user_input:
        print("Thanks for compliment Ghost!")

    
    
    else:
        print("I don't understand\nCan you say it again please!")


def action(user_input):
    parts = user_input.split(maxsplit=1)
    if len(parts) != 2:
        print("Unknown command please try again:")
        return

    verb, app_name = parts
    if verb not in act_words:
        print("Unknown command please try again:")
        return

    try:
        subprocess.Popen([apps[app_name]])
        print("Opening " + app_name.title() + "...")
    except KeyError:
        print("Unknown app, please try again:")
    except FileNotFoundError:
        print("App is not installed or cannot be started.")


    
while True:
    user_input = input("You: ").strip().lower()
    if not user_input:
        print("Please type something.")
        continue

    if any(user_input.startswith(word + " ") for word in act_words):
        action(user_input)
    
    elif user_input in exit_commands:
        print("Good Bye Ghost!")
        break
    else:
        chat_brain(user_input)