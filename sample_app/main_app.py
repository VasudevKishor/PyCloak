from utils import Formatter, get_user_id

def run_app():
    user_id = get_user_id()
    print(f"User ID: {user_id}")

    formatter = Formatter()
    greeting = formatter.format_greeting("Vasudev")
    print(greeting)

if __name__ == "__main__":
    run_app()
