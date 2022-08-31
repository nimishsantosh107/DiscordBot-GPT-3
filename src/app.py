import os

def app():
    print(os.environ.get('BOT_TOKEN'))

if __name__ == "__main__":
    app()