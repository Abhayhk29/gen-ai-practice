from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from pprint import pprint
from langchain.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model



load_dotenv()

queries = ['Tell me about the Apple 18 max pro phone']

def search_for_articles(queries):
    tavily_search = TavilySearch(
        max_results=3,
        topic="news",
        search_depth="basic",
        timeframe="week",
        include_raw_content=False,
        include_answer=False,
    )

    all_results = []
    for query in queries:
        results = tavily_search.invoke(query)
        all_results.append(results)

    # for results in all_results:
    #     print("Search results:")
    #     print("-------------------------")
    #     pprint(results)
    #     for result in results:
    #         print(f"Title: {result}")
    #     print("-------------------------")
    return all_results

def generate_newsletter(search_results):
    model = init_chat_model(
        "gemini-3.6-flash",
        model_provider="google_genai",
    )

    system_prompt = f"""
        You are a helpful assistant that generates a newsletter based on the search results provided.

        {search_results}

        Please create a newsletter that summarizes the key points from the search results.
        The newsletter should be well-structured, engaging, and informative.

    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Search results: {search_results}"),
        HumanMessage(content="Please generate a newsletter based on the search results.")
    ]

    response = model.invoke(system_prompt)
    if isinstance(response.content, list):
        return response.content[0]['text']
    return response


context = search_for_articles(queries)
# print("Search results:")
# pprint(context)
newsletter = generate_newsletter(context)
print(newsletter)

with open('newsletter.md', 'w', encoding='utf-8') as file:
    file.write(newsletter)
