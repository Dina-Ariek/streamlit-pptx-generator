import numpy as np

# Tambahkan lebih banyak topik dummy
extra_topics = [
    "mobil listrik", "pengisian cepat", "garansi", "dealer", "ketersediaan", "after-sales",
    "investor", "IPO", "kendala", "pengguna", "kualitas", "layanan", "navigasi", "aplikasi",
    "pembaruan software", "kecepatan", "jaringan", "pengiriman", "varian", "model baru"
]
all_topics = topics + extra_topics

# Generate lebih banyak edges dengan bobot acak
edges_weighted_extended = []
for _ in range(100):  # Tambah 100 edge baru
    a, b = random.sample(all_topics, 2)
    weight = random.randint(1, 10)
    edges_weighted_extended.append((a, b, weight))

# Buat graph baru
G_ext = nx.Graph()
for a, b, w in edges_weighted + edges_weighted_extended:
    if G_ext.has_edge(a, b):
        G_ext[a][b]['weight'] += w
    else:
        G_ext.add_edge(a, b, weight=w)

# Hitung bobot total untuk setiap node
node_weight_ext = {}
for node in G_ext.nodes:
    node_weight_ext[node] = sum([G_ext[node][nbr]['weight'] for nbr in G_ext.neighbors(node)])

# Normalisasi ukuran node
node_sizes_ext = [min_size + (node_weight_ext[n] / max(node_weight_ext.values())) * (max_size - min_size) for n in G_ext.nodes]

# Visualisasi network graph yang lebih besar
plt.figure(figsize=(14, 12))
pos_ext = nx.spring_layout(G_ext, seed=42, k=0.4)

nx.draw_networkx_nodes(G_ext, pos_ext, node_size=node_sizes_ext, node_color='skyblue')
nx.draw_networkx_edges(G_ext, pos_ext, width=[G_ext[u][v]['weight'] * 0.3 for u, v in G_ext.edges], edge_color='gray')
nx.draw_networkx_labels(G_ext, pos_ext, font_size=9, font_weight='bold')

plt.title("Network Graph Topik Terkait Brand VinFast (Versi Diperluas)", fontsize=16)
plt.axis("off")
plt.tight_layout()
plt.show()
