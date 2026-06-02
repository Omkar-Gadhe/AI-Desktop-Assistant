import subprocess
print("Welcome Ghost")

assistant_name = "AIRA"

responses = {
    "hi": f"Nihao, I am {assistant_name}",
    "how are you": "I'm fine\nHow about you?",
    "who are you": "Your Assistant\nHow can I help you?"
}

action ={
      "open firefox":"firefox",
      "open vscode":"code"

  }

act_words = ("launch", "open", "run")
def auto(user_input):


    subprocess.Popen(["code"])
    subprocess.Popen(["firefox"])

while True:
    user_input = input("You: ").strip().lower()

    if any(user_input.startswith(word + " ") for word in act_words):
        auto(user_input)
    

    if user_input in responses:
        print(responses[user_input])

    elif "good morning" in user_input:
        print("Good Morning Ghost!")

    elif "beautiful" in user_input:
        print("Thanks for compliment Ghost!")

    elif user_input == "bye":
        print("Good Bye Ghost!")
        break
    
    else:
        print("I don't understand\nCan you say it again please!")

