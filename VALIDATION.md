# Validation record

Verified on 10 November 2026 using this project's Python 3.12.8 virtual environment on Windows.

## Results

| Check | Result |
|---|---|
| Install the four frameworks into `.venv` | Passed |
| `python -m pip check` | Passed: no broken requirements |
| `python -m unittest discover -s tests -v` | Passed: 9 deterministic tests, no model requests |
| Active Python files compile | Passed |
| All module/function docstrings present | Passed |
| All four lesson imports and `--help` commands | Passed |
| LangChain pipeline construction | Passed |
| CrewAI construction: two agents and two tasks | Passed |
| Graph affordable offline CLI: Goa, 3 days, INR 15000 | Passed: estimate 7500, writer path, three day lines |
| Graph low-budget offline CLI: Goa, 3 days, INR 3000 | Passed: warning path, no writer |
| Local key matches the authorized BIA source | Passed; key value was never printed |
| Markdown code fences and required documents | Passed structural checks |

## Live framework executions

Each script was executed with Goa, two days and INR 10000, using the configured `gpt-4o-mini` model. The execution checker supplied CLI arguments and ran each script's actual main entry point. It captured terminal output and recorded only status/length, keeping exception messages and credentials out of the report.

| Script | Status | Captured output length |
| `01_langchain_plan.py` | Passed | 939 characters |
| `02_langgraph_workflow.py` | Passed | 958 characters |
| `03_autogen_team.py` | Passed | 1897 characters |
| `04_crewai_crew.py` | Passed | 1033 characters |

The checks establish that the model requests and framework orchestration completed. They do not certify travel facts, arithmetic in generated prose, availability, or identical future output. Live API access and credit should be checked again before teaching.

## Deterministic test coverage

The nine tests cover: complete affordable itinerary; low-budget path skipping the writer; exact budget equality; one rupee below the threshold; low-budget live setting requiring no model; one/seven-day limits; invalid city/day/budget values; city whitespace and offline switch parsing; and a clear missing-key error.

The tests run the actual compiled LangGraph. Model configuration is forbidden in the offline routing checks, so an accidental paid-model path fails the test. No external test framework is needed; the suite uses Python's built-in unittest.

## Environment and preservation notes

Direct requirements are pinned; `requirements-lock.txt` records transitive versions for Python 3.12 Windows. Package installation needed network access outside the restricted shell. An initial CrewAI import attempted its default AppData storage; configuration was corrected to the ignored local `.crewai` folder, and local crew construction passed afterward.

Automatic approval review rejected permanent deletion of the original notebooks/source/tests because it could discard useful material. The safe alternative was completed: originals are preserved in `legacy_archive`, outside the active teaching sequence. No deletion remains necessary for the demos. Exclude that archive, `.env`, `.venv`, `.crewai` and Python caches from student handouts.

Mermaid blocks are editable source diagrams. Markdown structure was checked; rendering depends on a viewer with Mermaid support. Tests do not run the preserved legacy exercises.
