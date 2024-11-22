import networkx as nx
import matplotlib.pyplot as plt
import random


#Generate a financial network
def generate_financial_network(num_nodes, num_edges):
    G = nx.DiGraph()  # Directed graph for transactions
    for i in range(num_nodes):
        G.add_node(i, institution=f"Inst_{i+1}")
    for _ in range(num_edges):
        # Ensure unique source-target pairs
        source, target = random.sample(range(num_nodes), 2)
        amount = random.randint(100, 10000)  # Transaction amount
        G.add_edge(source, target, amount=amount)
    return G


# Anomaly detection

# Nodes with high degree
def detect_high_degree_nodes(G, threshold=5):
    anomalies = [node for node, degree in G.degree() if degree > threshold]
    return anomalies

# Paths lenght analysis
def detect_long_paths(G, max_length=3):
    long_paths = []
    for source in G.nodes:
        for target in G.nodes:
            if source != target:
                try:
                    length = nx.shortest_path_length(G, source=source, target=target)
                    if length > max_length:
                        long_paths.append((source, target, length))
                except nx.NetworkXNoPath:
                    continue  # No path exists between these nodes
    return long_paths


# Graph visualization
def visualize_graph(G, anomalies, long_paths):
    pos = nx.spring_layout(G)  # Layout for nodes
    plt.figure(figsize=(12, 8))
    
    # Draw nodes and edges
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=700)
    
    # Highlight anomalies (high-degree nodes)
    nx.draw_networkx_nodes(G, pos, nodelist=anomalies, node_color="red")
    
    # Highlight edges involved in long paths
    long_path_edges = [(source, target) for source, target, _ in long_paths]
    nx.draw_networkx_edges(G, pos, edgelist=long_path_edges, edge_color="orange", width=2)
    
    # Add edge labels for transaction amounts
    edge_labels = nx.get_edge_attributes(G, "amount")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.title("Financial Network with Anomaly Detection")
    plt.show()


# Main program
if __name__ == "__main__":
    # Parameters for the network
    num_nodes = 10
    num_edges = 15
    
    # Generate the financial network
    G = generate_financial_network(num_nodes, num_edges)
    
    # Detect anomalies
    high_degree_anomalies = detect_high_degree_nodes(G, threshold=3)
    long_path_anomalies = detect_long_paths(G, max_length=3)
    
    # Print detected anomalies
    print("High-degree anomalies (excessive clustering):", high_degree_anomalies)
    print("Long transaction paths (length > 3):", long_path_anomalies)
    
    # Visualize the financial network
    visualize_graph(G, high_degree_anomalies, long_path_anomalies)