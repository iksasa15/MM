"""
Personal Assistant with Sub-Agents (Supervisor pattern).
Run the supervisor with a query; it routes to calendar or email sub-agents as needed.
"""
import os
import sys

# Check API key before importing agents (agents create the model at import time)
if not os.environ.get("OPENROUTER_API_KEY") and not os.environ.get("OPENAI_API_KEY"):
    print("Set OPENROUTER_API_KEY or OPENAI_API_KEY in the environment.")
    print("Example: export OPENAI_API_KEY=sk-...")
    sys.exit(1)

from langchain_core.messages import HumanMessage

from agents import supervisor_agent


def run_query(query: str):
    """Send a query to the supervisor and print the conversation."""
    result = supervisor_agent.invoke({"messages": [HumanMessage(content=query)]})
    messages = result.get("messages", [])
    for msg in messages:
        _print_message(msg)
    return result


def _print_message(msg):
    """Pretty-print a single message (Human, AI, or Tool)."""
    cls = type(msg).__name__
    if "Human" in cls:
        print("\n======== Human ========\n")
        print(getattr(msg, "content", msg))
    elif "AI" in cls or "AIMessage" in cls:
        print("\n======== AI ========\n")
        content = getattr(msg, "content", None)
        tool_calls = getattr(msg, "tool_calls", []) or []
        if tool_calls:
            for tc in tool_calls:
                name = tc.get("name", "?")
                args = tc.get("args", {})
                print(f"Tool: {name}")
                print(f"Args: {args}")
        if content:
            print(content)
    elif "Tool" in cls:
        print("\n======== Tool result ========\n")
        print(getattr(msg, "content", msg))
    print()


def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        run_query(query)
        return

    # Demo: single-domain and multi-domain
    print("=== Example 1: Schedule only ===")
    run_query("Schedule a team standup for tomorrow at 9am")

    print("\n" + "=" * 60)
    print("=== Example 2: Schedule + Email ===")
    run_query(
        "Schedule a meeting with the design team next Tuesday at 2pm for 1 hour, "
        "and send them an email reminder about reviewing the new mockups."
    )


if __name__ == "__main__":
    main()
