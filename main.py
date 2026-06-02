print("Welcome Ghost")

assistant_name = "AIRA"

responses = {
    "hi": f"Nihao, I am {assistant_name}",
    "how are you": "I'm fine\nHow about you?",
    "who are you": "Your Assistant\nHow can I help you?"
}

while True:
    user_input = input("You: ").strip().lower()

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