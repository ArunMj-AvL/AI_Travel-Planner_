# Quick start

```powershell
.\.venv\Scripts\python.exe 01_langchain_plan.py --destination Goa --days 3 --budget 15000
.\.venv\Scripts\python.exe 02_langgraph_workflow.py --destination Goa --days 3 --budget 15000 --offline
.\.venv\Scripts\python.exe 02_langgraph_workflow.py --destination Goa --days 3 --budget 3000 --offline
.\.venv\Scripts\python.exe 02_langgraph_workflow.py --destination Goa --days 3 --budget 15000
.\.venv\Scripts\python.exe 03_autogen_team.py --destination Jaipur --days 2 --budget 10000
.\.venv\Scripts\python.exe 04_crewai_crew.py --destination Kochi --days 2 --budget 10000
```

# Trainer guide: Session 18

The quick start above contains only run commands, in teaching order, with inputs. Run them from `session18_practical_kit` after setup. Students do not type into an interactive prompt: the three terminal options are their inputs.

## Learning outcome

By the end, a fresher should explain how a prompt becomes text, how a graph shares information and chooses a path, how two agents take turns, and how tasks pass results between roles. They should run each script, alter an input, identify the model call, and describe the output without calling it verified travel information.

Four frameworks in three hours is an introduction, not mastery. Spend most of the explanation on Python values and data flow. The common helper and source comments reduce the amount students must remember.

## Before class

Prepare the environment before the three-hour session. Follow README setup, verify `.env`, run the tests and rehearse the live commands. Check `VALIDATION.md` for any unresolved live API issue. Do not begin a paid demo until the account has model access and API credit. Open only the four top-level lessons, `common.py`, student guide and design document. Keep `legacy_archive` closed.

Use the same Python executable for install and execution. Show the source at a readable font size. Share `.env.example`, never `.env`, and hide the key file during screen sharing. Installing CrewAI may take time because its own dependency tree is large; do not spend the live session teaching its unused dependencies.

## 180-minute lesson plan

| Minutes | Duration | Activity and observable result |
|---|---:|---|
| 0?15 | 15 | Problem statement, one-traveller scope, estimates, HLD; students trace input to output |
| 15?30 | 15 | Explain terminal options, `common.py`, a function, dictionary and return value |
| 30?55 | 25 | LangChain: read source, run, change destination, identify prompt/model/parser |
| 55?90 | 35 | LangGraph: trace state, run both offline paths and a live plan, predict threshold behavior |
| 90?100 | 10 | Break |
| 100?125 | 25 | AutoGen: two roles, shared conversation, await, two-turn stopping limit |
| 125?150 | 25 | CrewAI: roles, task ownership, context handover, sequential process |
| 150?170 | 20 | Guided student exercise and comparison across frameworks |
| 170?180 | 10 | Demonstrate checks, recap assessment, questions |

## Opening explanation

Use this example: ?A person wants three days in Goa with INR 15,000 for expenses inside the city. We want a readable suggested itinerary. We are learning ways to arrange AI work, not building a booking engine.?

Explain that the framework is Python software, the model is the remote text service, and an agent combines a model with a role and instructions. A graph node can be ordinary Python with no AI. Two agents may share one model; they are not two different trained models.

Draw `terminal -> validated inputs -> chosen framework -> terminal output`. The lessons are independent versions of that same flow. Do not imply lesson 1 saves a plan for lesson 2; nothing is persisted between runs.

## Demo 1: LangChain, 25 minutes

1. Read the module docstring. Explain imports as bringing named tools into this file.
2. Open `build_chain`. Point to the system instruction and `{request}` placeholder.
3. Point to `ChatOpenAI` and the parser. Read `prompt | llm | parser` left to right.
4. Run the first quick-start command. Show that `invoke`, not construction, makes the request.
5. Change Goa to Mysuru, days to 2 and budget to 10000. Ask students to predict what stays the same.

Expected output: a short day-by-day itinerary with estimated costs. Exact wording changes. Have the class check the number of days and cost arithmetic themselves. Temperature zero reduces randomness but does not promise identical text.

Checkpoint: the student can explain why `invoke` receives a dictionary with a `request` key and why the final answer is a string.

## Demo 2: LangGraph, 35 minutes

Start offline so everyone can follow deterministic routing. Draw the graph from the design document and keep it beside the source. Explain `TripState` as a shared worksheet: the input fields arrive first, then nodes fill in `estimated_cost` and `final_plan`.

Run budget 15000, three days, offline. It prints `estimate_cost`, then `write_plan`, sample cost 7500 and three day lines. Run budget 3000, three days, offline. It prints `estimate_cost`, then `budget_warning`; the writer never runs. Trace the exact comparison: `7500 > 3000` is true.

Try budget 7500, three days, offline. Equality uses the writer branch because the condition is `>`, not `>=`. Then run the live command and show that the graph routing stays the same while the writer changes from fixed text to AI text.

Read `compile` as ?prepare the graph? and `invoke` as ?run the graph.? Emphasize that return values contain changed keys; LangGraph keeps the existing fields. `TypedDict` describes a structure; it does not perform runtime input validation.

Checkpoint: ask which node would run with two days and budget 4000. Correct: cost 5000, then warning, zero model requests.

## Demo 3: AutoGen, 25 minutes

Read `run_team` from top to bottom. The client is the connection to the model. The planner and reviewer have different instructions but share that client. Round-robin means fixed speaking order. With two agents and `max_turns=2`, planner speaks once, then reviewer speaks once.

Run the Jaipur command. Point out the two headings and the stop reason. The reviewer receives the original task and the previous message in the conversation. Show why printing only agent sources skips the original user message.

Explain `async def` as a function designed to wait for network work, `await` as waiting for that result, and `asyncio.run` as the starter for this async function in a Python script. `finally` closes the client even when a request fails. A short conceptual explanation is enough; do not introduce concurrent scheduling internals.

Checkpoint: ask whether setting `max_turns=4` would create four agents. Correct: no, it allows four total agent turns. Keep the classroom code at two to avoid extra requests.

## Demo 4: CrewAI, 25 minutes

Read the `LLM`, then the two `Agent` objects. Role is a job title, goal is the desired result and backstory adds a brief working context. `allow_delegation=False` keeps the handover explicit. `max_iter=2` limits agent iterations; it is not a universal hard cap on billable calls.

Point to each `Task`: description says what to do, expected_output describes the form, and agent says who owns it. `context=[draft]` supplies the draft output to the review. `Process.sequential` fixes execution order. `kickoff` runs the crew; `result.raw` is the final task's text.

Run the Kochi command. If framework status messages appear, focus on the final reviewed text. Compare it with AutoGen: the team organizes speaking turns; the crew organizes owned tasks and their context. Neither automatically proves arithmetic or live availability.

Checkpoint: ask why the review needs both the original trip brief and draft context. It must check the draft against the actual request.

## Guided exercise, 20 minutes

Give everyone `--destination Mysuru --days 2 --budget 10000`. Run lesson 2 offline first, then choose one paid demo per student/pair if API access is available. Compare the number of days and whether the result labels prices as estimates.

Have students change lesson 1's system message to request exactly three short bullet points while preserving the estimate warning. They should explain which component changed and whether the input parser changed. Restore the original prompt after the exercise.

Have students predict and run `--days 0` and `--budget -100`. The parser should stop before model requests. Run the deterministic tests at the end. Students can explain why those tests do not need an API key.

## Assessment and teaching pitfalls

A successful student can identify all of these: a validated input, a prompt placeholder, a model request, a returned dictionary update, a conditional edge, the reviewer turn, the context handover and the final printed value.

Avoid saying a graph must contain AI or an agent has real autonomy beyond our code. Avoid treating model prose as structured validated output. Do not call the sample cost a destination-specific quote. Do not promise a two-agent reviewer will always find mistakes. No lesson executes model-written code.

## Recovery during class

If live API calls fail, read the matching README troubleshooting entry and use lesson 2 offline. Continue tracing the other scripts and their diagrams, but say clearly that these source walkthroughs are not live framework executions. Rehearse the live demos again after fixing the account/network issue. Do not quietly substitute fake AI responses.

## Optional follow-up after the three hours

Let students add a deterministic food-cost field to the graph, then explain where it belongs in state and how its output changes the estimate. Persistence, RAG, retries/backoff, live search and deployments belong to later sessions.
