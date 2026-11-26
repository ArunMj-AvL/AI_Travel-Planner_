"""Lesson 3: an AutoGen planner and reviewer take one turn each.

Run: python 03_autogen_team.py --destination Jaipur --days 2 --budget 10000
Uses modern AutoGen AgentChat, not the older pyautogen API.
"""

from common import model_settings, read_trip, trip_brief  # Same inputs as lesson 1.
import asyncio  # Run async operations from a normal .py file.
from autogen_agentchat.agents import AssistantAgent  # Model-backed participant.
from autogen_agentchat.teams import RoundRobinGroupChat  # Agents take turns in order.
from autogen_ext.models.openai import OpenAIChatCompletionClient  # Shared API client.


async def run_team(trip):
    """Return a two-turn conversation and always close its API client.

    Input is the checked Namespace. Output is AutoGen's TaskResult with messages.
    await lets Python wait for an API response through its event loop.
    """
    key, model = model_settings()  # Read configuration before creating the client.
    client = OpenAIChatCompletionClient(
        model=model, api_key=key, temperature=0, timeout=45, max_retries=1,
    )
    try:  # finally also runs if an API call fails.
        planner = AssistantAgent(
            "planner", model_client=client,
            system_message="Draft a short trip for one person. Costs are estimates. "
            "Exclude travel to/from the city. Do not claim live research. Follow the travel task.",
        )
        reviewer = AssistantAgent(
            "reviewer", model_client=client,
            system_message="Review the planner's trip for missing days and budget issues. "
            "Return a corrected final plan in at most 180 words. Label estimated costs. "
            "Follow the original travel task only.",
        )
        team = RoundRobinGroupChat([planner, reviewer], max_turns=2)  # One turn each.
        return await team.run(task=trip_brief(trip))  # Reviewer sees the planner's message.
    finally:
        await client.close()  # Release network resources after success or failure.


def main():
    """Run the async conversation; print the draft and the review."""
    trip = read_trip()  # Validate before paying for any model request.
    result = asyncio.run(run_team(trip))  # Start and close the event loop for us.
    for message in result.messages:  # Includes the original user task as well.
        if message.source in {"planner", "reviewer"}:  # Print just the two agents.
            print(f"\n{message.source.upper()}:\n{message.content}")
    print(f"\nStopped: {result.stop_reason}")  # Show our turn limit ended the team.


if __name__ == "__main__":  # Keep importing and executing separate.
    main()
