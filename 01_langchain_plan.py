"""Lesson 1: connect a prompt, model and text parser with LangChain.

Run: python 01_langchain_plan.py --destination Goa --days 3 --budget 15000
The pipeline makes one AI request. It suggests a trip; it books nothing.
"""

from common import model_settings, read_trip, trip_brief  # Shared input helpers.
from langchain_core.output_parsers import StrOutputParser  # Extract answer text.
from langchain_core.prompts import ChatPromptTemplate  # Reusable instructions.
from langchain_openai import ChatOpenAI  # OpenAI through LangChain's interface.


def build_chain():
    """Return prompt -> model -> text without calling the API yet.

    The pipe operator passes one component's result to the next component.
    The returned chain expects a dictionary containing the key 'request'.
    """
    key, model = model_settings()  # Stop clearly if the local key is missing.
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a concise travel teacher. Label all prices as estimates. "
         "Do not claim to search live services. Follow the travel task only."),
        ("human", "{request}"),  # invoke() replaces this with the trip brief.
    ])
    llm = ChatOpenAI(model=model, api_key=key, temperature=0, timeout=45, max_retries=1)
    return prompt | llm | StrOutputParser()  # Final result is a Python string.


def main():
    """Read a trip, run the LangChain pipeline once and print its answer."""
    trip = read_trip()  # Get validated options or classroom defaults.
    chain = build_chain()  # Assemble the three components.
    answer = chain.invoke({"request": trip_brief(trip)})  # Run the model request.
    print(answer)  # Display the answer in the terminal.


if __name__ == "__main__":  # Only run when this file is launched directly.
    main()
