import base64
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


load_dotenv()

image_path = "images/test.jpg"
with open(image_path, "rb") as f:
    image_bytes = f.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")


model = init_chat_model(
    model="gpt-4.1-nano",
    model_provider="openai")

messages = [{"role": "user", "content": [
    {"typpe": "text", "text": "describe what you have seen in the images"},
    {"type":"image", "base64": image_base64, "mime_type": "image/jpeg"}
]}]

response = model.invoke(messages)
print(response.content)