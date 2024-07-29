import os

from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_vertexai import ChatVertexAI
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_documents():
    pdf_folder_path = os.getenv("PDF_FOLDER_PATH", default="")
    if not pdf_folder_path:
        raise ValueError("PDF_FOLDER_PATH not set in environment variables")

    documents = []
    for file in os.listdir(pdf_folder_path):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder_path, file)
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())

    return documents

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
        persist_directory="pdf_embeddings"
    )

def retrieve_and_generate(question):
    llm = ChatVertexAI(model="gemini-1.5-flash")
    embedding = VertexAIEmbeddings(
        model_name="textembedding-gecko@001",
        project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    )
    vectorstore = Chroma(
        persist_directory="pdf_embeddings",
        embedding_function=embedding,
    )
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
    prompt = hub.pull("rlm/rag-prompt")

    def format_docs(docs):
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
