import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage

from tools import (
    search_flights,
    book_flight,
    search_hotels,
    book_hotel,
    estimate_trip_cost,
)

# اكتب مفتاح Gemini هنا مباشرة (استبدل النص بين علامات التنصيص)
GEMINI_API_KEY = "AIzaSyD78kK36D92yf2Fq0OQ6Jv1ZvR9k8QZuEI"

genai.configure(api_key=GEMINI_API_KEY)

model_gemini = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
)

FLIGHT_AGENT_PROMPT = (
    "You are a flight booking assistant. "
    "You help users find and book flights using natural language requests. "
    "Parse dates, cities, and budget into proper parameters. "
    "Use search_flights to find options and summarize them clearly. "
    "When the user explicitly asks to book, call book_flight with the chosen offer_id. "
    "Always explain your choice and show price and duration."
)

flight_agent = create_agent(
    model=model_gemini,
    tools=[search_flights, book_flight],
    system_prompt=FLIGHT_AGENT_PROMPT,
)

HOTEL_AGENT_PROMPT = (
    "You are a hotel booking assistant. "
    "You choose suitable hotels based on location, budget, and dates. "
    "Use search_hotels to find candidates. "
    "When the user confirms booking, call book_hotel. "
    "Always summarize hotel name, area, rating, and price per night."
)

hotel_agent = create_agent(
    model=model_gemini,
    tools=[search_hotels, book_hotel],
    system_prompt=HOTEL_AGENT_PROMPT,
)

BUDGET_AGENT_PROMPT = (
    "You are a budget assistant for trips. "
    "You combine flight and hotel costs and compare with the user budget. "
    "Use estimate_trip_cost to compute totals. "
    "Explain clearly whether the plan fits the budget or suggest adjustments."
)

budget_agent = create_agent(
    model=model_gemini,
    tools=[estimate_trip_cost],
    system_prompt=BUDGET_AGENT_PROMPT,
)

def run_flight_agent(request: str) -> str:
    result = flight_agent.invoke({"messages": [HumanMessage(request)]})
    return result["messages"][-1].text

def run_hotel_agent(request: str) -> str:
    result = hotel_agent.invoke({"messages": [HumanMessage(request)]})
    return result["messages"][-1].text

def run_budget_agent(request: str) -> str:
    result = budget_agent.invoke({"messages": [HumanMessage(request)]})
    return result["messages"][-1].text