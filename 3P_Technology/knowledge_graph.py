import networkx as nx
from typing import Dict, List, Tuple
from pyvis.network import Network

class KnowledgeGraph:
    def __init__(self):
        self.G = nx.DiGraph()

    def add_project(self, project: Dict):
        pid = project['project_id']
        self.G.add_node(pid, **project)

        # Link industry node
        industry = project.get('industry')
        if industry:
            inid = f"industry:{industry}"
            self.G.add_node(inid, type='industry')
            self.G.add_edge(pid, inid, rel='belongs_to')

        # Link platform nodes
        for p in project.get('platforms', []):
            pnode = f"platform:{p}"
            self.G.add_node(pnode, type='platform')
            self.G.add_edge(pid, pnode, rel='uses')

    def common_platforms(self, industry: str) -> List[Tuple[str, int]]:
        counts = {}
        for pid, d in self.G.nodes(data=True):
            if d.get('project_id') and d.get('industry') == industry:
                for plat in d.get('platforms', []):
                    counts[plat] = counts.get(plat, 0) + 1
        return sorted(counts.items(), key=lambda x: x[1], reverse=True)

    # --------------------------------------------------------
    #             NEW: PyVis graph visualization
    # --------------------------------------------------------
    def visualize_graph(self, output_html: str = "kg_graph.html"):
        net = Network(height="700px", width="100%", directed=True)
        net.toggle_physics(True)
    
        # Add nodes
        for node, data in self.G.nodes(data=True):
            ntype = data.get("type", "project")
    
            color = {
                "industry": "#ffcc00",
                "platform": "#00ccff",
                "project": "#66cc66"
            }.get(ntype, "#cccccc")
    
            shape = {
                "industry": "diamond",
                "platform": "triangle",
                "project": "dot"
            }.get(ntype, "dot")
    
            net.add_node(
                node,
                label=node,
                color=color,
                shape=shape,
                title=str(data)
            )
    
        # Add edges
        for src, dst, data in self.G.edges(data=True):
            rel = data.get("rel", "")
            net.add_edge(src, dst, label=rel)
    
        # ❗ THIS IS CRITICAL
        net.write_html(output_html)
    
        return output_html
