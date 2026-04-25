from langchain.chat_models import init_chat_model

GOOGLE_API_KEY = 'AIzaSyCG0DullANSHD0ePJTGl6F0crGjHzG-QGg'

model = init_chat_model(
                model="gemini-3-flash-preview", 
                model_provider="google-genai", 
                google_api_key=GOOGLE_API_KEY 
            )

with open("test.txt") as file:
    input_text = file.read()
response = model.invoke(f"which having best scope in the future in india context what will be the probable salary for 10 years of experience? {input_text}")
print(response.content)
