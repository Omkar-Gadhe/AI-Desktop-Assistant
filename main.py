print("Welcome Ghost,")
ghost_l = ["hi","who are you","bye","how are you"]

while True:
    ghost = input().strip().lower()
    if ghost in ghost_l or "beautiful" in ghost or "good morning" in ghost:
      if ghost == "hi":
          print("Nihao,I am AIRA")
      elif "good morning" in ghost:
          print("Good Morning Ghost!")
      elif ghost == "how are you":
          print("I'm fine\nHow about you:")
      elif "beautiful" in ghost:
          print("Thanks for compliment Ghost!")
      elif ghost == "who are you":
          print("Your Assistant\nHow can i help you:")
    
      elif ghost == "bye":
          print("Good Bye Ghost!")
          exit()
    else:
        print("I don't understand\ncan you say it again please!")