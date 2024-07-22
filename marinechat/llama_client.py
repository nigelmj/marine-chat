import os
from langchain_experimental.llms import ChatLlamaAPI
from llamaapi import LlamaAPI

llama = LlamaAPI(os.environ.get("LLAMA_API_KEY"))
model = ChatLlamaAPI(client=llama)
