import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import os

load_dotenv()

def get_weather(city: str):
    # This is a placeholder function. In a real implementation, you would call a weather API here.
    """Get weather of given city
    """
    api_key = os.getenv("OPENWEATHERMAP_API_KEY");
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    reponse = requests.get(base_url, params=params)
    data = reponse.json()
    # print(data)
    return data
    return f"The weather in {city} is sunny with a high of 25°C."

def get_location():
    # This is a placeholder function. In a real implementation, you would call a geolocation API here.
    """Get current location of user. Use this tool when user ask about weather without providing city name
    """
    response = requests.get("https://ipapi.co/json", headers={'User-agent': 'yout-bot 0.1'}) #it mimick the browser
    data = response.json()
    return f"{data['city']}, {data['country']}"

# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2, google_api_key=os.getenv("GOOGLE_API_KEY"))
# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# response = llm.invoke("What is the capital of France?")
# print(response.content)

# here two calls happening Reasoning and Action call, in reasoning call agent will decide which tool to use and in action call it will call the tool and get the response and then it will give the final response to user
# we provide docs to agent and it will decide which tool to use based on user query and docs provided to it, here we are providing get_weather tool to agent and if user query is related to weather then it will call get_weather tool and give the response to user



system_prompt = """You are a helpful assistant that provides information about weather and location. You have access to two tools: get_weather and get_location. Use get_weather tool to get the weather of a city and use get_location tool to get the current location of the user. If the user asks about weather without providing city name, use get_location tool to get the current location of the user and then use get_weather tool to get the weather of that location. 
                    Always provide accurate and concise information to the user.
                    2.If the user provides the city name, use get_weather tool to get the weather of that city. If the user asks about location, use get_location tool to get the current location of the user. Always provide accurate and concise information to the user.
                    3. use  ur knowledge to determine which temperature unit to use (Celsius or Fahrenheit) based on the user's location. For example, if the user is in the United States, use Fahrenheit, and if the user is in Europe, use Celsius.

"""
# # agent = create_agent(llm , tools=[get_weather], agent_type="zero-shot-react-description", verbose=True)
agent = create_agent(llm , tools=[get_weather, get_location], system_prompt={system_prompt}, checkpointer=InMemorySaver())

# ressponse1 = agent.invoke({
#     "messages": [{"role": "user", "content": "What is the weather?"}]
# })

# print(ressponse1)

user_query = input("Enter your query: ")

response = agent.invoke(
    {"messages": [{"role": "user", "content": user_query}]},{"configurable": {"thread_id": "1"}}
)

print(response['messages'][-1])