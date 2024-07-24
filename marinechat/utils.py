import bs4
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Only keep post title, headers, and content from the full HTML.

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
    embedding = VertexAIEmbeddings(model_name="textembedding-gecko@001")
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=embedding)
    vectorstore.persist()

def index_documents():
    docs = load_documents()
    all_splits = split_documents(docs)
    store_documents(all_splits)
