from app import create_app, db
from config import AppConfig

app = create_app(AppConfig)

if __name__ == "__main__":
    app.run("127.0.0.1", "5000", debug=True)