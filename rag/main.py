from pathlib import Path
from pypdf import PdfReader

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import SystemMessage, HumanMessage
load_dotenv()  # Load environment variables from .env file

def read_documents_from_directory():
    directory = Path('My Documents')
    documents = []
    for file in directory.rglob('*'):
        if file.suffix in {'.txt', '.pdf', '.docx'}:
            if file.suffix == '.pdf':
                reader = PdfReader(file)
                content = "\n".join(page.extract_text() for page in reader.pages)
                # print(f"Found PDF file: {file.name}")
            else:
                # content = file.read_text(encoding='utf-8', errors='ignore')
                content = file.read_text()
                # print(f"Found text file: {file.name}")
            documents.append({
                "path": str(file.relative_to(directory)),
                "content": content
            })

    print(documents)


# big_string = """
# This is a long string that contains multiple lines of text.
# Chant and be happy. ABCD for Devotees A : Association B : Book C : CHanting D : Diet
# """

# system_prompt = """
# You are a helpful assistant that answers questions about the company and its products.
# {big_string}
# """

# messages = [
#     SystemMessage(content=system_prompt),
# ]

# user_query = input("Enter your question: ")
# messages.append(HumanMessage(content=user_query))


# llm = ChatGoogleGenerativeAI(
#     model="gemini-3.6-flash")


# response = llm.invoke(messages)

# print(response)

