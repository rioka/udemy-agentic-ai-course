import openai
import os
import openai.types.chat
from pypdf import PdfReader
import gradio
import pathlib

def main() -> None:

    google_api_url = os.getenv('GOOGLE_HOST', 'https://generativelanguage.googleapis.com/v1beta/openai/')
    google_api_key = os.getenv('GOOGLE_API_KEY')

    if google_api_key is None:
        print("Missing Google API key: cannot proceed")
        return

    SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
    gemini = openai.OpenAI(api_key=google_api_key, base_url=google_api_url)
    model_name = "gemini-2.5-flash"

    # question = "When did Italian defender Antonello Cuccureddu retire?"
    # messages = [openai.types.chat.ChatCompletionUserMessageParam(role = "user", content = question)]

    # response = gemini.chat.completions.create(model=model_name, messages=messages)
    # answer = response.choices[0].message.content

    # print(answer)

    print('Reading CV...')
    cv = read_cv(f'{SCRIPT_DIR.parent}/me/cv_2025.pdf')

    print('Reading summary...')
    summary = read_text(f'{SCRIPT_DIR.parent}/me/summary.txt')

    name = "Riccardo Dozzo"

    system_prompt = get_system_prompt(name, cv, summary)

    answer = chat(gemini, model_name, system_prompt, 'What would you focus on in the first 3 months in a new position?', [])
    print(answer) 

    #gradio.ChatInterface(chat).launch()

    # This question is not answered properly, because it does not know who I am referring to,
    # because this is a *new* conversation for Gemini
    # question = "What did he do after retiring?"
    # messages = [openai.types.chat.ChatCompletionUserMessageParam(role = "user", content = question)]

    # response = gemini.chat.completions.create(model=model_name, messages=messages)
    # answer = response.choices[0].message.content

    # print(answer)

def read_cv(file: str) -> str:

    reader = PdfReader(file)
    cv = ""
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            cv += text

    return cv

def read_text(file: str) -> str:
    
    with open(file, "r", encoding="utf-8") as f:
        return f.read()

def get_system_prompt(name: str, cv: str, summary: str) -> str:

    system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
    particularly questions related to {name}'s career, background, skills and experience. \
    Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
    You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
    Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
    If you don't know the answer, say so."

    system_prompt += f"\n\n## Summary:\n{summary}\n\n## Curriculum Vitae:\n{cv}\n\n"

    return system_prompt + f"With this context, please chat with the user, always staying in character as {name}."

def chat(client: openai.OpenAI, model: str, system_prompt, message, history):
    """Chat with LLM.

    Args:
        client (openai.OpenAI): An OpenAI instance
        model (str): The model to use
        system_prompt (str): System prompt
        message (str): Message for LLM
        history (str): Previous questions and answers 

    Returns:
        str: The response from the LLM
    """
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    response = client.chat.completions.create(model=model, messages=messages)

    return response.choices[0].message.content

if __name__ == "__main__":
    main()
