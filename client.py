import requests

API_URL = "http://localhost:5002"  # Replace with your API URL


history = []


while True:
    question = input("Enter your question (or 'exit' to quit): ")
    if question.lower() == 'exit':
        break

    history.append({"role": "user", "content": question})

    response = requests.post(f"{API_URL}/ask", json={"question": question})
    assistant_response = response.json().get('message').get('content')
    history.append({"role": "assistant", "content": assistant_response})
    print(f"Assistant: {assistant_response}")

# response = requests.post(f"{API_URL}/ask", json={"question": "What is the capital of France?"})

# print(response.json())