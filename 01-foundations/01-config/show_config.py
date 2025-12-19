import dotenv
import os

def main() -> None:

    if dotenv.load_dotenv(override=True):
        openai_api_key = try_get_key('OPENAI_API_KEY')
        anthropic_api_key = try_get_key('ANTHROPIC_API_KEY')
        google_api_key = try_get_key('GOOGLE_API_KEY')
        deepseek_api_key = try_get_key('DEEPSEEK_API_KEY')
        groq_api_key = try_get_key('GROQ_API_KEY')
    else:
        print("Unable to load .env file")

def try_get_key(key: str) -> str | None:
     
     value = os.getenv(key)
     
     if value:
            print(f"Key {key} exists and begins with {value[:8]}")
     else:
            print(f"Key {key} not set")
     
     return value

if __name__ == "__main__":
    main()
