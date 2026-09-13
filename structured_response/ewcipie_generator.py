from dotenv import load_dotenv
# from langchain_ollama import Ollama
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing import List, Optional
load_dotenv()  # Load environment variables from .env file

class Reciepe(BaseModel):
    """A Single  Reciepe"""
    name: str = Field(description="Name of the recipe")
    description: str = Field(default=None, description="Description of the recipe")
    prep_time : str = Field(default=None, description="Preparation time for the recipe")

class Response(BaseModel):
    """A Single  Reciepe"""
    ingredients: List[str] = Field(description="List of ingredients")
    recipes: List[Reciepe] = Field(description="List of recipes suggested")


model = init_chat_model(
    model="llama3.2:1b",
    model_provider="ollama"
)

structured_response = model.with_structured_output(Response)

system_prompt = """
"You are a helpful chef, Identify the main indegrediatnts. Suggest 3 recipes that can be made with the main ingredients. Suggest 3 alternative ingredients for each main ingredient"
"""

message = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "I have paneer, wheat and peas?"}
]

result = structured_response.invoke(message)
print(result)
# print(result.model_dump_json(indent=2))