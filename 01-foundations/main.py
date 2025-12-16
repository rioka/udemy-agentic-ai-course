import dotenv
import os

def main() -> None:

    loaded = dotenv.load_dotenv(override=True)
    
    if loaded:
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key:
            print(f"OpenAI API Key exists and begins with {openai_api_key[:8]}")
        else:
            print("OpenAI API Key not set")
    else:
        print("Unable to load .env file")

if __name__ == "__main__":
    main()
