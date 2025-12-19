import setup

def chat(message, history):
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
    messages = [{"role": "system", "content": setup.get_system_prompt()}] + history + [{"role": "user", "content": message}]
    response = setup.get_client().chat.completions.create(model=setup.get_model(), messages=messages)

    return response.choices[0].message.content
