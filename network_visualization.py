import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.request
import tarfile
import os

# geting data
url = "https://snap.stanford.edu/data/twitter.tar.gz"
filen = "twitter.tar.gz"
folder = "twitter"

if not os.path.exists(filen):
    urllib.request.urlretrieve(url, filen)

if not os.path.exists(folder):
    with tarfile.open(filen, "r:gz") as filen:
        filen.extractall()

# .edges files available
edges = [f for f in os.listdir(folder) if f.endswith('.edges')]

# cego network 
sample_file = os.path.join(folder, edges[0])  # pick 1st ego network
G = nx.read_edgelist(sample_file)

degree = dict(G.degree())  # find degree

# filtered graph by degree threshold
threshold = 5
filtered_nodes = [n for n, d in degree.items() if d > threshold]
filtered_subgraph = G.subgraph(filtered_nodes)

plt.figure(figsize=(10, 6))
pos = nx.spring_layout(filtered_subgraph, seed=42)
nx.draw_networkx_nodes(
    filtered_subgraph, pos,
    node_size=[degree[n] * 20 for n in filtered_subgraph.nodes()],
    node_color='lightblue'
)
nx.draw_networkx_edges(filtered_subgraph, pos, alpha=0.5)
nx.draw_networkx_labels(filtered_subgraph, pos, font_size=8)
plt.title(f"Filtered Ego-Twitter Network (Degree > {threshold})")
plt.axis('off')
plt.tight_layout()
plt.savefig("filtered_ego_network.png", dpi=300)
plt.close()

# degree distribution
plt.figure(figsize=(8, 5))
sns.histplot(list(degree.values()), bins=20, kde=True, color="skyblue")
plt.title("Node Degree Distribution")
plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("degree_distribution.png", dpi=300)
plt.close()

# top 15 nodes b centrality
centrality = nx.betweenness_centrality(G, k=100, seed=42)  # find betweenness centrality
filtered_centrality = {n: centrality[n] for n in filtered_subgraph.nodes()}
top_nodes = sorted(filtered_centrality.items(), key=lambda x: x[1], reverse=True)[:15]
top_names = [node for node, _ in top_nodes]
top_scores = [score for _, score in top_nodes]

plt.figure(figsize=(8, 5))
sns.barplot(x=top_names, y=top_scores, palette="Oranges_d")
plt.title("Top 15 Nodes by Betweenness Centrality (Filtered Graph)")
plt.xlabel("Node")
plt.ylabel("Centrality")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top15_centrality.png", dpi=300)
plt.close()
