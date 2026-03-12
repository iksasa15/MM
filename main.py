from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage

from agents import (
    model_gemini,
    run_flight_agent,
    run_hotel_agent,
    run_budget_agent,
)

@tool
def plan_flight(request: str) -> str:
    """Plan or book flights using natural language."""
    return run_flight_agent(request)

@tool
def plan_hotel(request: str) -> str:
    """Plan or book hotels using natural language."""
    return run_hotel_agent(request)

@tool
def check_budget(request: str) -> str:
    """Check if a proposed trip fits the budget."""
    return run_budget_agent(request)

SUPERVISOR_PROMPT = (
    "You are a travel planning supervisor agent. "
    "You can coordinate three capabilities: flights, hotels, and budget evaluation. "
    "Use plan_flight for flight-related actions, plan_hotel for lodging, "
    "and check_budget to verify the plan against a given budget. "
    "Break down complex travel requests into multiple tool calls when needed, "
    "and then synthesize a final, coherent travel plan in your answer. "
    "Clearly separate sections for Flights, Hotels, and Budget in the final response."
)

supervisor_agent = create_agent(
    model=model_gemini,
    tools=[plan_flight, plan_hotel, check_budget],
    system_prompt=SUPERVISOR_PROMPT,
)

if __name__ == "__main__":
    q1 = "Find me a flight from Riyadh to Tokyo around June 10 under $800."
    r1 = supervisor_agent.invoke({"messages": [HumanMessage(q1)]})
    print("=== Example 1 ===")
    for m in r1.get("messages", []):
        print(m.type.upper(), ":\n", getattr(m, "text", ""), "\n")

    q2 = (
        "Plan a 5-day trip to Tokyo from Riyadh around June 10. "
        "Find a reasonable flight and a mid-range hotel in Shinjuku. "
        "Keep the total trip under $2000."
    )
    r2 = supervisor_agent.invoke({"messages": [HumanMessage(q2)]})
    print("=== Example 2 ===")
    for m in r2.get("messages", []):
        print(m.type.upper(), ":\n", getattr(m, "text", ""), "\n")