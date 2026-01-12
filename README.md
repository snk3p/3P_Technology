# Self-Learning Impact Analysis System (RAG + LLM) — Submission

**Assignment used**: Technical Assignment — LLM & RAG Implementation. 

This project implements a **Self-Learning Impact Analysis System for Industrial Automation** for industrial automation projects, featuring: RAG-based knowledge search, tender text parsing, learning metrics, and a knowledge graph.

-----
## The project structure and deliverables include the working prototype code
- Knowledge base with 10 example projects (`data/example_projects.json`)
- Knowledge Query (RAG) pipeline (`rag_pipeline.py`)
- Tender Parser (extracts I/O points, protocols, redundancy, response time)(`parser.py`)
- Knowledge Graph implementation and visualization (`knowledge_graph.py`)
- Streamlit Learning Metrics Dashboard (`app.py`)
- ROI computation (`roi_calculation.md`)

## Features available in the dashboard:
- Metrics: Projects count, average hour delta, on-time rate.
- Knowledge Growth: Line chart of cumulative facts over time.
- Error Reduction Simulation: Bar chart showing before/after performance.
- Project Explorer: Select a project and view details.
- Knowledge Query (RAG): Ask questions about the knowledge base.
- Tender Parser: Paste tender text to extract I/O points, protocols, redundancy, response time.
- Knowledge Graph: Interactive visualization of projects, industries, and platforms.


🚀 ## How to run (local)
1. Create virtualenv and install:
```bash
python -m venv 3P
source 3P/bin/activate

Clone the repository.
Ensure data/example_projects.json exists.

Run the dashboard:
streamlit run app.py


Tender Text Parser
We require 128 I/O points, Profinet and OPC UA. Response time 50 ms. N-1 redundancy.



Knowledge Query (RAG)
Ask a question about the knowledge base:
Users can ask natural language questions like:
What common issues occur in chemical industry PLC projects?
Which platform causes most delays?

Requirements:
Python 3.9+
Streamlit
Pandas
NetworkX
PyVis
Matplotlib
pip install streamlit pandas networkx pyvis matplotlib
pip install -r requirements.txt


## Notes
This is a prototype for demonstration. Replace LLM API calls with your API keys and cloud vector DB for production.
