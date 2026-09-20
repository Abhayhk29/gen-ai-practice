# from pathlib import Path
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# from langchain.messages import SystemMessage, HumanMessage
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.vectorstores import InMemoryVectorStore
# # from langchain_community.document_loaders import DirectoryLoader, PyPDFDirectoryLoader, TextLoader
# import glob
# from langchain_unstructured import UnstructuredLoader

# load_dotenv()  # Load environment variables from .env file


# llm = ChatGoogleGenerativeAI(
#     model="gemini-3.6-flash",
# )


# directory = 'My Documents'
# # load documents from a directory
# # directory = Path('My Documents')
# pdf_loader = glob.glob(f"{directory}/**/*.pdf", recursive=True)
# dir_loader = UnstructuredLoader(pdf_loader)
# pdf_documents = dir_loader.load()

# text_loader = UnstructuredLoader(directory, glob="**/*.txt")
# # text_loader = DirectoryLoader(directory, glob="**/*.txt", loader_cls=TextLoader)
# text_documents = text_loader.load()

# text_docs = pdf_documents + text_documents


# # creating embeddings and vector store
# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# vector_store = InMemoryVectorStore(embeddings)
# vector_store.add_documents(text_docs)


# # get user query
# user_query = input("Enter your question: ")

# retrieved_docs = vector_store.similarity_search(user_query, k=3)

# context = "\n".join(doc.page_content for doc in retrieved_docs)

# system_prompt = f""" You are a helpful assistant that answers questions {context}
# """


# messages = [
#     SystemMessage(content=system_prompt)]

# messages.append(HumanMessage(content=user_query))

# response = llm.invoke(messages=messages)
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_unstructured import UnstructuredLoader

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

directory = Path("My Documents")
file_paths = [
    str(path)
    for path in directory.rglob("*")
    if path.suffix.lower() in {".pdf", ".txt"} and path.is_file()
]

if not file_paths:
    raise FileNotFoundError(f"No PDF or TXT files found under {directory.resolve()}")

# UnstructuredLoader takes file path(s), not a directory + glob
loader = UnstructuredLoader(file_paths)
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = InMemoryVectorStore.from_documents(chunks, embeddings)

user_query = input("Enter your question: ")
retrieved_docs = vector_store.similarity_search(user_query, k=3)
context = "\n\n".join(doc.page_content for doc in retrieved_docs)

system_prompt = f"""You are a helpful assistant. Answer the user's question using only the context below.
If the context does not contain the answer, say you don't know.

Context:
{context}
"""

messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content=user_query),
]

response = llm.invoke(messages)
print(response.content)