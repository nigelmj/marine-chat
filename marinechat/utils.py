import bs4
import os

from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_vertexai import ChatVertexAI
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# TODO: Switch to loading required PDFs
def load_documents():
    bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))
    loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs={"parse_only": bs4_strainer},
    )
    return loader.load()

def split_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)
    return all_splits

def store_documents(all_splits):
    embedding = VertexAIEmbeddings(
        model_name="textembedding-gecko@001",
        project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    )
    vectorstore = Chroma.from_documents(
        documents=all_splits,
        embedding=embedding,
        persist_directory="vectordb"
    )

def retrieve_and_generate(question):
    llm = ChatVertexAI(model="gemini-1.5-flash")
    embedding = VertexAIEmbeddings(
        model_name="textembedding-gecko@001",
        project='ragworkflow',
    )
    vectorstore = Chroma(
        persist_directory="vectordb",
        embedding_function=embedding,
    )
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
    prompt = hub.pull("rlm/rag-prompt")

    def format_docs(docs):
        print(doc.page_content for doc in docs)
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = ""
    for chunk in rag_chain.stream(question):
        answer += chunk
    return answer
