from source.API import API
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    api = API()
    api.run()