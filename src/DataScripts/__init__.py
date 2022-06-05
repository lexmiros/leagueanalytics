from riotwatcher import LolWatcher, ApiError
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

watcher = LolWatcher(api_key)
