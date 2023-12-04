from dotenv import load_dotenv
import os

env = os.getenv("FLASK_ENV", "development")
print(env)

if env == "test":
    load_dotenv(dotenv_path="test.env")
else:
    load_dotenv(dotenv_path="dev.env")

APP_NAME = os.environ.get("APP_NAME")
DATABASE_URI = os.environ.get("DATABASE_URI")
PORT = os.environ.get("PORT")
SECRET_KEY = os.environ.get("SECRET_KEY")
