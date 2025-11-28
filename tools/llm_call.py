import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

base_url = "https://aipipe.org/openrouter/v1/chat/completions"
fallback_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

api_key = os.getenv("IITM_API_KEY")
fallback_api_key = os.getenv("GEMINI_API_KEY")

iitm_client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

gemini_client = OpenAI(
    api_key=fallback_api_key,
    base_url=fallback_url
)

def llm_call(messages, model="claude-sonnet-4-5"):
    try:
        response = iitm_client.chat.completions.create(
            model=model,
            messages=messages
        )
    except Exception as e:
        print(f"Primary model failed: {e}. Switching to fallback.")
        response = gemini_client.chat.completions.create(
            model="gemini-2.0-flash-exp",
            messages=messages
        )
    return response

def talk_with_llm(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    response = llm_call(messages)
    return response.choices[0].message.content

if __name__ == "__main__":
    print(talk_with_llm("Hello, how are you?"))
