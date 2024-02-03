

def main():
    with open("game/Play.py") as f:
        code = compile(f.read(), "game/Play.py", "exec")
        exec(code)

if __name__ == "__main__":
    main()

