"""Lesson 4: two CrewAI agents perform explicit tasks in sequence.

Run: python 04_crewai_crew.py --destination Kochi --days 2 --budget 10000
The same travel project is expressed as roles, tasks and task context.
"""

from common import model_settings, read_trip, trip_brief  # Shared classroom helpers.
from crewai import Agent, Crew, LLM, Process, Task  # Five building blocks.


def build_crew(trip):
    """Return a sequential crew containing two agents and two tasks.

    The review receives the draft's output through context=[draft].
    No tool or code execution is enabled. kickoff() starts the model requests.
    """
    key, model = model_settings()  # Same key and model as the other lessons.
    llm = LLM(model=f"openai/{model}", api_key=key, temperature=0, timeout=45)
    planner = Agent(
        role="Travel planner", goal="Create a simple trip with estimated local costs.",
        backstory="You teach beginners to plan trips. Never claim live research.",
        llm=llm, allow_delegation=False, max_iter=2, verbose=False,
    )
    reviewer = Agent(
        role="Budget reviewer", goal="Check days and costs and present the final trip.",
        backstory="You explain budget concerns clearly and label all prices as estimates.",
        llm=llm, allow_delegation=False, max_iter=2, verbose=False,
    )
    draft = Task(
        description=trip_brief(trip),  # Task 1 carries the user's actual inputs.
        expected_output="A short day-by-day draft with estimated INR costs.",
        agent=planner,  # This role owns the drafting task.
    )
    review = Task(
        description="Check the draft against this original request: " + trip_brief(trip)
        + " Correct missing days or budget problems. Do not promise affordability if costs exceed budget.",
        expected_output="A corrected final itinerary and a budget note, in at most 180 words.",
        agent=reviewer, context=[draft],  # Hand the completed draft to the reviewer.
    )
    return Crew(
        agents=[planner, reviewer], tasks=[draft, review],
        process=Process.sequential,  # Finish drafting before reviewing.
        memory=False, cache=False, verbose=False, tracing=False,
    )


def main():
    """Read the trip, execute two tasks and print the final task's text."""
    trip = read_trip()  # All lessons accept the same three terminal options.
    result = build_crew(trip).kickoff()  # CrewAI coordinates the task handover.
    print(result.raw)  # CrewOutput.raw holds the final review text.


if __name__ == "__main__":  # Run only when launched directly.
    main()
