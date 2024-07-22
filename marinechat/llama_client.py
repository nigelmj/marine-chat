import os
from langchain_experimental.llms import ChatLlamaAPI
from llamaapi import LlamaAPI

llama = LlamaAPI(os.environ.get("LLAMA_API_KEY"))
model = ChatLlamaAPI(client=llama)

SYSTEM_PROMPT = (
    "You are a highly accurate and detailed information retrieval assistant. "
    "For each query, provide precise, comprehensive, and contextually relevant information. "
    "Ensure that your responses are well-structured and cover all necessary aspects of the topic."
)

def query_with_system_prompt(prompt):
    full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
    return model.invoke(full_prompt, max_tokens=2048)
