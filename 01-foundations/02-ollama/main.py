import openai
import os
import openai.types.chat
#import IPython.display
from IPython.display import Markdown, display

def main() -> None:

    ollama_host = os.getenv('OLLAMA_HOST')
    model_name = os.getenv('OLLAMA_MODEL', 'llama3.2:1b')

    question = get_question(f'{ollama_host}/v1', model_name)

    print(question)

    if question is None:
        print("No question to ask")
        return

    answer = send_question(f'{ollama_host}/v1', model_name, question)
    print(answer)
    ##IPython.display.display(IPython.display.Markdown(answer))
    #display(Markdown(answer))
    #competitors.append(model_name)
    #answers.append(answer)

def get_question(host: str, model: str) -> str | None:

    request = "Please come up with a challenging, nuanced question that I can ask a number of LLMs to evaluate their intelligence. "
    request += "Answer only with the question, no explanation."
    messages: list[openai.types.chat.ChatCompletionMessageParam] = [{"role": "user", "content": request}]

    client = openai.OpenAI(base_url=host, api_key='ollama')
    response = client.chat.completions.create(model=model, messages=messages)

    return response.choices[0].message.content

def send_question(host: str, model: str, question: str) -> str | None:

    messages: list[openai.types.chat.ChatCompletionMessageParam] = [{"role": "user", "content": question}]
    client = openai.OpenAI(base_url=host, api_key='ollama')
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content

if __name__ == "__main__":
    main()
