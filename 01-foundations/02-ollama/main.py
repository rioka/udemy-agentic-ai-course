import openai
import os
import openai.types.chat
# from IPython.display import Markdown, display

def main() -> None:

    ollama_host = os.getenv('OLLAMA_HOST')
    model_name = os.getenv('OLLAMA_MODEL', 'llama3.2:1b')

    question = get_question(f'{ollama_host}/v1', model_name)

    print(f"**Question**:\n{question}\n")

    if question is None:
        print("No question to ask")
        return

    answer = send_question(f'{ollama_host}/v1', model_name, question)
    # Using plain `print` here, because we're running it from the console
    print(f"**Answer**:\n{answer}\n")
    # display(Markdown(answer))
    #competitors.append(model_name)
    #answers.append(answer)

    if answer is None:
        print("No answer was provided")
        return

    evaluation = evaluate_response(f'{ollama_host}/v1', 'llama3.2', question, answer)

    if evaluation is None:
        print("No evaluation was provided")
        return

    print(f"**Evaluation**:\n{evaluation}")

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

def evaluate_response(host: str, model: str, question: str, answer: str) -> str | None:

    judge = f"""You are judging an answer tothis question:

    {question}

    Your job is to evaluate the response for clarity and strength of argument, and rank it.
    Respond with JSON, and only JSON, with the following format:
    {{"grade": "...", "evaluation": "..."}}
    where 
    - "grade" is a letter A to F, A being the best and F the worst
    - "evaluation" is your explanation for the grade you've assigned
    
    Here is the response you must evaluate:

    {answer}

    Now respond with the JSON I've given, nothing else."""

    messages: list[openai.types.chat.ChatCompletionMessageParam]  = [{"role": "user", "content": judge}]

    client = openai.OpenAI(base_url=host, api_key='ollama')
    response = client.chat.completions.create(
        model=model, 
        messages=messages
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    main()
