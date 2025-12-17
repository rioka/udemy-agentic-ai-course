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

    ##IPython.display.display(IPython.display.Markdown(answer))
    #display(Markdown(answer))
    #competitors.append(model_name)
    #answers.append(answer)

def get_question(host: str, model: str) -> str | None:

    request = "Please come up with a challenging, nuanced question that I can ask a number of LLMs to evaluate their intelligence. "
    request += "Answer only with the question, no explanation."
    messages: list[openai.types.chat.ChatCompletionMessageParam] = [{"role": "user", "content": request}]

    ollama = openai.OpenAI(base_url=host, api_key='ollama')
    response = ollama.chat.completions.create(model=model, messages=messages)

    return response.choices[0].message.content

if __name__ == "__main__":
    main()
