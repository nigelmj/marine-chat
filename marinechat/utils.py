import os

from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_vertexai import ChatVertexAI
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from marinechat.schemas import QuotedAnswer

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
    structured_llm = llm.with_structured_output(QuotedAnswer)

    embedding = VertexAIEmbeddings(
        model_name="textembedding-gecko@001",
        project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    )
    vectorstore = Chroma(
        persist_directory="pdf_embeddings",
        embedding_function=embedding,
    )
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

    system_prompt = (
        "You're a helpful AI assistant. Given a user question "
        "and some maritime document snippets, answer the user "
        "question. If none of the articles answer the question, "
        "just say you don't know."
        "\n\nHere are the documents: "
        "{context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{question}"),
        ]
    )

    def format_docs_with_id(docs) -> str:
        formatted = [
            f"Source ID: {i}\nDocument Title: {doc.metadata['source']}\nDocument Snippet: {doc.page_content}"
            for i, doc in enumerate(docs)
        ]
        return "\n\n" + "\n\n".join(formatted)

    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: format_docs_with_id(x["context"])))
        | prompt
        | structured_llm
    )

    retrieve_docs = (lambda x: x["question"]) | retriever

    chain = RunnablePassthrough.assign(context=retrieve_docs).assign(
        answer=rag_chain_from_docs
    )

    result = chain.invoke({"question": question})
    return result
