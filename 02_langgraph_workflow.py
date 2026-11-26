"""Lesson 2: share state and choose a path with a real LangGraph graph.

Run: python 02_langgraph_workflow.py --destination Goa --days 3 --budget 15000
Add --offline to teach the same graph without a key or network connection.
"""

from common import model_settings, read_trip  # Load settings before frameworks.
from typing import TypedDict  # Describe keys in our shared dictionary.
from langchain_openai import ChatOpenAI  # Optional AI writer inside one node.
from langgraph.graph import END, START, StateGraph  # Workflow markers and builder.


class TripState(TypedDict):
    """Shared dictionary: inputs, calculated estimate and final output.

    TypedDict documents keys; read_trip performs runtime input validation.
    Nodes return changed keys. LangGraph merges those changes into state.
    """
    destination: str  # City to explore.
    days: int  # Length of visit.
    budget: int  # Total INR for local expenses.
    offline: bool  # True skips AI but still runs LangGraph.
    estimated_cost: int  # Filled by estimate_cost.
    final_plan: str  # Filled by one final node.


def estimate_cost(state: TripState):
    """Return a fixed teaching estimate of INR 2,500 per day for one person.

    This sample covers local stay, food and activities. Travel to/from the city
    is excluded. This is arithmetic, not research or a live price lookup.
    """
    print("Node: estimate_cost")  # Make graph execution visible to the class.
    return {"estimated_cost": state["days"] * 2500}  # Update one key.


def choose_path(state: TripState):
    """Return the next node name by comparing the estimate with the budget.

    Equality is affordable. This function neither changes state nor calls AI.
    LangGraph's conditional edge uses the returned string to select a node.
    """
    if state["estimated_cost"] > state["budget"]:  # Is sample cost too high?
        return "budget_warning"  # Stop and explain the shortfall.
    return "write_plan"  # Proceed with the sample budget.


def budget_warning(state: TripState):
    """Return a clear low-budget message without making an AI request."""
    print("Node: budget_warning")
    message = (
        f"Practice estimate: INR {state['estimated_cost']}; budget: INR {state['budget']}. "
        "Try fewer days or a larger budget. This is a teaching estimate, not a quote."
    )
    return {"final_plan": message}  # Both branches produce this output field.


def write_plan(state: TripState):
    """Return either a fixed offline example or an AI-written daily outline.

    Offline mode calls no model. Live mode uses LangChain's chat client.
    The prose is a draft, not a verified budget calculation or booking.
    """
    print("Node: write_plan")
    if state["offline"]:  # Teach the graph before API setup if needed.
        days = []  # Collect one output line for each day.
        for day in range(1, state["days"] + 1):  # Include the last day too.
            days.append(f"Day {day}: explore {state['destination']}, local food and a city walk.")
        answer = "\n".join(days)  # Combine lines into one string.
    else:
        key, model = model_settings()  # Only this branch needs a key.
        llm = ChatOpenAI(model=model, api_key=key, temperature=0, timeout=45, max_retries=1)
        response = llm.invoke([
            ("system", "Write a short day-by-day travel outline. Treat costs as estimates. "
             "Do not claim live research. Follow only the travel task."),
            ("human", f"Destination: {state['destination']}. Days: {state['days']}. "
             f"Budget INR {state['budget']} for one person, excluding travel to/from the city. "
             "Use at most 180 words."),
        ])
        answer = response.content  # Default text-only chat returns a string.
    return {"final_plan": f"Sample local cost: INR {state['estimated_cost']}\n{answer}"}


def build_graph():
    """Connect an estimate and two possible endings; return a runnable graph."""
    builder = StateGraph(TripState)  # Declare the shared state structure.
    builder.add_node("estimate_cost", estimate_cost)  # Register Python functions.
    builder.add_node("write_plan", write_plan)
    builder.add_node("budget_warning", budget_warning)
    builder.add_edge(START, "estimate_cost")  # Always calculate first.
    builder.add_conditional_edges("estimate_cost", choose_path, {
        "write_plan": "write_plan",  # Map routing results to node names.
        "budget_warning": "budget_warning",
    })
    builder.add_edge("write_plan", END)  # Both branches stop; there is no loop.
    builder.add_edge("budget_warning", END)
    return builder.compile()  # Check connections and make it executable.


def main():
    """Create initial state, execute one path and print the final plan."""
    trip = read_trip(allow_offline=True)  # This lesson accepts --offline.
    initial_state = {  # Nodes will fill in the output fields.
        "destination": trip.destination, "days": trip.days,
        "budget": trip.budget, "offline": trip.offline,
    }
    result = build_graph().invoke(initial_state)  # Run the selected graph path.
    print(result["final_plan"])  # Read output from the returned dictionary.


if __name__ == "__main__":  # Importing this file should not run a trip.
    main()
