# Session 18: one travel project, four AI frameworks

A three-hour terminal workshop for absolute beginners. Learn LangChain, LangGraph, AutoGen and CrewAI using the same travel-planning problem. Each lesson is a short `.py` file with plain-English comments and function docstrings.

## Review outcome

The original kit used genuine LangGraph orchestration and LangChain model clients, but had no AutoGen or CrewAI examples. It also included two identical travel notebooks, a refactor notebook, random service failures, retry policies, multiple data models and a revision loop. That was too much for a first three-hour introduction.

The replacement keeps the travel theme and rewrites the notebook concepts into simpler Python lessons. Original material is preserved in `legacy_archive/` for trainer reference; exclude that folder from student distribution. See [AUDIT.md](AUDIT.md) for the original findings and replacement mapping.

## Setup: Windows PowerShell

Use Python 3.12, the interpreter tested on this machine. Start in BIA:

```powershell
cd .\session18_practical_kit
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The trainer's project already has its own `.venv` and a local `.env` with the required key copied from BIA. For a new student machine:

```powershell
Copy-Item .env.example .env
notepad .env
```

Set `OPENAI_API_KEY`. The lesson default is `OPENAI_MODEL=gpt-4o-mini`. Live demos need network access, model access and API credit; requests incur usage charges. Never share `.env`, `.crewai` or the trainer's virtual environment. Share `.env.example` and recreate the environment instead. Terminal environment variables override `.env`.

Use the exact `.venv` Python below. Activation is optional, so PowerShell execution-policy changes are unnecessary. On macOS/Linux, substitute `.venv/bin/python`.

## Run in order

```powershell
.\.venv\Scripts\python.exe 01_langchain_plan.py --destination Goa --days 3 --budget 15000
.\.venv\Scripts\python.exe 02_langgraph_workflow.py --destination Goa --days 3 --budget 15000 --offline
.\.venv\Scripts\python.exe 02_langgraph_workflow.py --destination Goa --days 3 --budget 3000 --offline
.\.venv\Scripts\python.exe 02_langgraph_workflow.py --destination Goa --days 3 --budget 15000
.\.venv\Scripts\python.exe 03_autogen_team.py --destination Jaipur --days 2 --budget 10000
.\.venv\Scripts\python.exe 04_crewai_crew.py --destination Kochi --days 2 --budget 10000
```

| File | Main concept | Visible result |
|---|---|---|
| `common.py` | Shared validation and settings | Used by all lessons |
| `01_langchain_plan.py` | Prompt -> model -> text pipeline | Generated itinerary |
| `02_langgraph_workflow.py` | State, nodes, conditional edge | Node trace and plan or warning |
| `03_autogen_team.py` | Agents and ordered conversation | Planner draft and reviewer correction |
| `04_crewai_crew.py` | Roles, tasks, context, process | Final reviewed itinerary |

Use the same input in all four for a direct comparison. These are alternative implementations of one project, not four frameworks joined into one complicated application.

## Boundaries

Inputs describe one traveller, 1?7 days and a positive integer INR budget. Budget covers local stay, food and activities; travel to/from the city is excluded. No bookings, dates, weather API, database, persistent memory, web search or UI are involved. All costs are teaching estimates. Only the graph applies a fixed INR 2,500/day rule. AI-written totals in other demos need human checking; a reviewer is another model call, not an accuracy guarantee.

`--offline` works only in lesson 2. It executes real LangGraph and replaces only the AI writer with a fixed city-walk outline. Other demos need the API. LangChain makes one request; the graph makes zero or one; AutoGen has two agent turns. CrewAI normally uses one model response per task, but may make additional requests through its iteration/retry behavior.

CrewAI may create internal bookkeeping files even with memory disabled. They are kept in the ignored local `.crewai/` folder. The application does not use them as conversation memory.

## Guides and checks

- [Trainer guide](trainer_guide.md): command-only quick start, example inputs, 180-minute timetable and demo cues.
- [Student guide](student_guide.md): concepts, design, every script and every function explained. Read source comments alongside it for statement-by-statement help.
- [Design document](design_document.md): problem statement, HLD, LLD, flowcharts, interfaces and limitations.
- [Validation](VALIDATION.md): actual verification results and live API status.

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

`requirements.txt` pins the tested direct dependencies. `requirements-lock.txt` records the resolved environment. Install the lock file to reproduce trainer versions on Python 3.12 Windows. CrewAI brings many transitive dependencies, including unused database packages; those are installation dependencies, not additional lesson topics.

## Troubleshooting

| Symptom | Action |
|---|---|
| `ModuleNotFoundError` | Use this folder's `.venv` Python and install requirements. |
| Missing key message | Edit this project's `.env`; check for an overriding terminal variable. |
| Authentication error / 401 | Replace the key with a valid API key. |
| Quota / 429 | Check API credit/rate limits; avoid repeatedly rerunning paid demos. |
| Timeout / connection error | Check network access; use lesson 2 with `--offline` meanwhile. |
| Unsupported model | Restore the tested default; other providers need code changes. |
| Input error | Use a nonempty city, 1?7 days and positive integer budget. |

## Official API references

[LangChain ChatOpenAI](https://docs.langchain.com/oss/python/integrations/chat/openai), [LangGraph graph API](https://docs.langchain.com/oss/python/langgraph/graph-api), [AutoGen agents](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/agents.html), [AutoGen teams](https://microsoft.github.io/autogen/stable/reference/python/autogen_agentchat.teams.html), [CrewAI crews](https://docs.crewai.com/en/concepts/crews), [CrewAI LLMs](https://docs.crewai.com/en/concepts/llms).
