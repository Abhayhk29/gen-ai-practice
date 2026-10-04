import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent


load_dotenv()  # Load environment variables from .env file


llm = init_chat_model(
    "gemini-3.6-flash",
    model_provider="google_genai",
    temperature=0.5,
)

def list_directory_contents(path: str=".") -> str:
    """
    Lists the contents in the given directory.Default is the current working directory.
    """
    result = "Contents of the directory:\n"
    items = os.listdir(path)

    files = []
    directories = []

    for item in items:
        if os.path.isfile(item):
            files.append(item)
        elif os.path.isdir(item):
            directories.append(item)

    if directories:
        result = "Directories:\n" + "\n".join(directories) + "\n\n"
    if files:
        result += "Files:\n" + "\n".join(files)

    # items_str = "\n".join(items)
    return result

agent = create_agent(
    model=llm,
    tools=[list_directory_contents],
)


user_input = "Give me list of files and folders in the current working directory."


messages = [
    {"role": "user", "content": user_input}
]


# response = agent.invoke({"messages": messages})
response2 = list(agent.stream({"messages":messages}))
print("Agent Response:")
for chunk in response2:
    for step, data in chunk.items():
        if step == "tools":
            result = data['messages'][-1].content
            print(f"Tool Output: {result}")
        elif step == 'model':
            msg = data['messages'][-1]
            if msg.tool_calls:
                print(f"Tool: {msg.tool_calls[0]['name']}")
                # print(data['message'][-1])
            else:
                print(f"Model message: {msg.content}")

    # print(chunk)