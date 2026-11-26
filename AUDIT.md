# Session 18 code audit

Reviewed on 10 November 2026 before preparing the new lessons.

| Original material | Finding | Replacement |
|---|---|---|
| `travel_planner.ipynb`, `baseline/travel_planner.ipynb` | Identical files; each has 22 cells, 1,449 code lines | Four short `.py` lessons |
| `travel_planner_refactor_workshop.ipynb` | 17 cells, 45 code lines; imports old source utilities | Trainer/student guides |
| `src/graph.py` | Genuine LangGraph; research, fallback, plan, critique, revise, finalize | Estimate and conditional plan/warning graph |
| `src/llm.py`, `src/nodes.py` | Genuine LangChain clients; Ollama default, optional OpenAI | One OpenAI configuration |
| Retry, guard and configuration modules | Backoff/jitter, wrapped exceptions, random failure switches | Omitted from beginner teaching path |
| State module | Several Pydantic models and output normalization | One TypedDict and argparse checks |
| Tool module | Mock flights/hotels and activities, not live travel searches | Clearly labelled fixed-cost estimate |
| Original tests | Test removed utilities; graph test could call live LLM | Deterministic routing/input checks |
| Framework coverage | No AutoGen or CrewAI | Real AgentChat team and sequential CrewAI crew |

## Correctness and teaching concerns

The original critique function created its model client outside its exception handler, so setup errors could escape the advertised fallback. Its revision loop could repeat a fallback critique without improving the plan. The graph test disabled random tools without isolating model access. The notebooks included old sample dates, repeated compilation and demo cells, a long regex parser and mock travel services that overwhelmed the framework lesson. Requirements allowed major-version drift without a tested lock file.

Original files, including their old README and environment template, are preserved under `legacy_archive/`. They are not part of the supported run sequence and their old tests are not discovered by the new test command. This preserves the trainer's source while removing unnecessary code from the active lesson. Do not distribute the archive to freshers.

## Notebook-to-Python mapping

- Natural language/regex extraction -> `common.read_trip`, using clear terminal options.
- Shared state and graph wiring -> `TripState` and `build_graph` in lesson 2.
- Search and cost processing -> one deterministic, explicitly sample-cost node.
- Itinerary presentation -> lesson 1's pipeline and lesson 2's writer node.
- Critique/refinement -> one planner/reviewer handover in lessons 3 and 4.
- Notebook image displays -> Mermaid diagrams in the teaching documents.

This is a curated rewrite, not an unedited cell export. It deliberately reduces features. Modern AutoGen AgentChat is used; older `pyautogen`/AG2 examples are not drop-in replacements.
