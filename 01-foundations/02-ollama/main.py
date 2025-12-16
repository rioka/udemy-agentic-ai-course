import openai
import os
from openai.types.chat import ChatCompletionMessageParam  # <-- typed dict

def main() -> None:

    request = "Please come up with a challenging, nuanced question that I can ask a number of LLMs to evaluate their intelligence. "
    request += "Answer only with the question, no explanation."
    messages: list[ChatCompletionMessageParam] = [{"role": "user", "content": request}]    

    model_name = "llama3.2" # 3B / 2GB
    ollama_host = os.getenv('OLLAMA_HOST')
    ollama = openai.OpenAI(base_url=f'{ollama_host}/v1', api_key='ollama')

    response = ollama.chat.completions.create(model=model_name, messages=messages)
    answer = response.choices[0].message.content

    #display(Markdown(answer))
    #competitors.append(model_name)
    #answers.append(answer)    