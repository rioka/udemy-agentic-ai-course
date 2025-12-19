import openai
import os
import pathlib
import pypdf

_google_api_url = os.getenv('GOOGLE_HOST', 'https://generativelanguage.googleapis.com/v1beta/openai/')
_google_api_key = os.getenv('GOOGLE_API_KEY')
_model_name = os.getenv('GOOGLE_MODEL', 'gemini-2.5-flash')

_SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
_doc_path = f'{_SCRIPT_DIR.parent}/me'

_client = openai.OpenAI(api_key=_google_api_key, base_url=_google_api_url)

def _read_cv(file: str) -> str:

    reader = pypdf.PdfReader(file)
    cv = ""
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            cv += text

    return cv

def _read_text(file: str) -> str:
    
    with open(file, "r", encoding="utf-8") as f:
        return f.read()

_cv = _read_cv(f"{_doc_path}/cv_2025.pdf")
_summary = _read_text(f"{_doc_path}/summary.txt")

def client() -> openai.OpenAI:
    return _client

name = 'Riccardo Dozzo'

def get_system_prompt() -> str:

    system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
    particularly questions related to {name}'s career, background, skills and experience. \
    Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
    You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
    Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
    If you don't know the answer, say so."

    system_prompt += f"\n\n## Summary:\n{_summary}\n\n## Curriculum Vitae:\n{_cv}\n\n"

    return system_prompt + f"With this context, please chat with the user, always staying in character as {name}."

def get_model() -> str:
    return _model_name

def get_client() -> openai.OpenAI:
    return _client
