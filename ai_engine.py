import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    token=os.getenv("HF_TOKEN")
)

def analyze_with_ai(messages):

    response = client.chat_completion(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=messages,
    )

    return response.choices[0].message["content"]