import os

# TODO, move to UI
print("WELCOME TO ZERO-SUM GAMES")
print("What would you like to Play?")
print("Options are")
items = os.listdir("games")
print(" ".join(items))

while True:
    name = input("Enter Game Name: ").strip()
    if os.path.isdir("games/" + name):
        with open("games/" + name + "/game/Play.py") as f:
            code = compile(f.read(), "games/" + name + "/game/Play.py", "exec")
            exec(code)
            break