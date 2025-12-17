import openai
import os
import openai.types.chat
# from IPython.display import Markdown, display

def main() -> None:

    ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.2:1b')

    localai_host = os.getenv('LOCALAI_HOST', 'http://localhost:8765')
    localai_model = os.getenv('LOCALAI_MODEL', 'dolphin3.0-qwen2.5-3b')

    question = get_question(f'{ollama_host}/v1', ollama_model)

    print(f"**Question**:\n{question}\n")

    if question is None:
        print("No question to ask")
        return
    
    answers = []

    print("**Asking Ollama**\n")
    answer = send_question(f'{ollama_host}/v1', ollama_model, question)
    # Using plain `print` here, because we're running it from the console
    if answer is None:
        print("No answer was provided")
        return

    print(f"**Answer (Ollama)**:\n{answer}\n")
    answers.append(answer)

    print("**Asking LocalAI**\n")
    answer = send_question(f'{localai_host}/v1', localai_model, question)
    if answer is None:
        print("No answer was provided")
        return

    print(f"**Answer (LocalAI)**:\n{answer}\n")
    answers.append(answer)

    evaluation = evaluate_response(f'{ollama_host}/v1', 'llama3.2', question, answers)

    if evaluation is None:
        print("No evaluation was provided")
        return

    print(f"**Evaluation**:\n{evaluation}")

def get_question(host: str, model: str) -> str | None:

    request = "Please come up with a challenging, nuanced question that I can ask a number of LLMs to evaluate their intelligence. "
    request += "Answer only with the question, no explanation."
    messages = [openai.types.chat.ChatCompletionUserMessageParam(role = "user", content = request)]

    client = openai.OpenAI(base_url=host, api_key='ollama')
    response = client.chat.completions.create(model=model, messages=messages)

    return response.choices[0].message.content

def send_question(host: str, model: str, question: str) -> str | None:

    messages = [openai.types.chat.ChatCompletionUserMessageParam(role = "user", content = question)]
    client = openai.OpenAI(base_url=host, api_key='ollama')
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content

def evaluate_response(host: str, model: str, question: str, answers: list[str]) -> str | None:

    judge = f"""You are judging an answer to this question:

    {question}

    Your job is to evaluate the response for clarity and strength of argument, and rank it.
    Respond with JSON, and only JSON, with the following format:
    {[{"grade": "...", "evaluation": "..."}]}
    where 
    - "grade" is a letter A to F, A being the best and F the worst
    - "evaluation" is your explanation for the grade you've assigned
    
    The order of your response must match the order of the responses, so the first element is for the first answer, 
    the second for the second answer, and so on.

    Here is the responses you must evaluate:

    {answers}

    Now respond with the JSON I've given, nothing else."""

    messages = [openai.types.chat.ChatCompletionUserMessageParam(role = "user", content = judge)]

    client = openai.OpenAI(base_url=host, api_key='ollama')
    response = client.chat.completions.create(
        model=model, 
        messages=messages
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    main()
