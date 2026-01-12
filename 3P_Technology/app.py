import streamlit as st
import pandas as pd
import json
from pathlib import Path
from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt
from extractor import load_projects
from rag_pipeline import RAGPipeline
from knowledge_graph import KnowledgeGraph
from parser import parse_tender_text
import streamlit.components.v1 as components
# ----------------------------
# Load & Configure Dashboard
# ----------------------------
DATA = Path("/Users/snk/Code/3P/3P_Technology/data/example_projects.json")

st.set_page_config(layout="wide", page_title="Learning Metrics Dashboard")
st.title("Self-Learning Impact Analysis System for Industrial Automation — Learning Metrics Dashboard")

projects = load_projects(str(DATA))
df = pd.DataFrame(projects)

# ----------------------------
# Metrics
# ----------------------------
st.metric("Projects in KB", len(df))
st.metric("Avg hour delta", round(df['hour_delta'].mean(), 1))
st.metric("On-time rate", f"{round((df['on_time'].mean()*100),1)}%")

# ----------------------------
# Knowledge Growth
# ----------------------------
st.header("Knowledge Growth")
growth = pd.DataFrame({
    'month': pd.date_range('2023-01-01', periods=12, freq='M'),
    'new_facts': [5,10,8,12,15,11,20,18,25,30,22,28]
})
growth['cumulative'] = growth['new_facts'].cumsum()
st.line_chart(growth.set_index('month')['cumulative'])

# ----------------------------
# Error Reduction
# ----------------------------
st.header("Error Reduction Simulation")
before = df['hour_delta'].abs().mean()
after = before * 0.65
st.bar_chart(pd.Series({'Before': before, 'After': after}))

# ----------------------------
# Project Explorer
# ----------------------------
st.header("Project Explorer")
sel = st.selectbox("Select project", df['project_id'].tolist())
p = df[df['project_id']==sel].iloc[0].to_dict()
st.json(p)

st.write("Download data: use `data/example_projects.json` in repo.")

# ===========================================================
#                Tender Parser Integration
# ===========================================================
st.header("Tender Text Parser")

# Input text box for tender descriptions
tender_text = st.text_area(
    "Paste tender text here to extract I/O, protocols, redundancy, and response time",
    height=150
)

if tender_text:
    parsed = parse_tender_text(tender_text)
    st.subheader("Parsed Tender Data")
    st.json(parsed)

# ===========================================================
#                RAG PIPELINE INTEGRATION
# ===========================================================
st.header("Knowledge Query (RAG)")

# ---- Create a simple in-memory vector DB for demo ----
class SimpleVectorDB:
    def __init__(self):
        self.data = []

    def add(self, doc_id, text):
        self.data.append({"id": doc_id, "text": text})

    def search(self, query, k=5):
        # naïve contains-based scoring for prototype
        hits = [d for d in self.data if query.lower() in d["text"].lower()]
        return hits[:k]

# ---- Initialize RAG with demo DB ----
db = SimpleVectorDB()
rag = RAGPipeline(db)

# Ingest documents (convert projects to RAG-ready docs)
docs_for_rag = [
    {
        "id": str(row["project_id"]),
        "text": row["description"] if "description" in row else json.dumps(row.to_dict())
    }
    for _, row in df.iterrows()
]

rag.ingest_docs(docs_for_rag)

# ---- UI for querying ----
user_query = st.text_input("Ask a question about the knowledge base:")

if user_query:
    result = rag.query(user_query)

    st.subheader("RAG Answer")
    st.write(result["answer"])

    st.subheader("Relevant Documents Retrieved:")
    for h in result["hits"]:
        st.json(h)

# ---------------------------------------------------------
# Knowledge Graph Integration
# ---------------------------------------------------------
kg = KnowledgeGraph()

# Add all projects to the KG
for _, row in df.iterrows():
    kg.add_project(row.to_dict())

st.header("Knowledge Graph Insights")

# Select industry to analyze
industries = sorted(df['industry'].dropna().unique())
selected_industry = st.selectbox("Select Industry", industries)

if selected_industry:
    common = kg.common_platforms(selected_industry)

    st.subheader(f"Most Common Platforms in {selected_industry}")
    if common:
        st.table(pd.DataFrame(common, columns=["Platform", "Count"]))
    else:
        st.info("No platform data found for this industry.")

# Optionally show raw graph stats
with st.expander("Knowledge Graph Stats"):
    st.write(f"Total nodes: {kg.G.number_of_nodes()}")
    st.write(f"Total edges: {kg.G.number_of_edges()}")

# ---------------------------------------------------------
# Knowledge Graph Visualization
# ---------------------------------------------------------
st.header("Knowledge Graph Visualization")

# Generate the HTML file
html_path = Path("kg_graph.html")
kg.visualize_graph(str(html_path))     # IMPORTANT: generate visualization

# Load and display the HTML file
if html_path.exists():
    components.html(
        html_path.read_text(),
        height=800,
        scrolling=True
    )
else:
    st.error("Knowledge graph HTML could not be generated.")
