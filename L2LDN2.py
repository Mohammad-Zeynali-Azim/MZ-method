# ------------------------------------Division Graph -----------------Row by Row------------------
import networkx as nx
import matplotlib.pyplot as plt


def draw_digit_transformation_graph(N, n):
    # Initialize directed graph
    G = nx.DiGraph()

    # Initialize current digits
    current_digits = [int(d) for d in str(N)]
    d = len(current_digits)

    # Add initial digits with labels (left to right)
    for idx, digit in enumerate(current_digits):
        node_id = f"iter0_digit{idx}"
        G.add_node(node_id, layer=0, label=str(digit), pos=(idx, 0))

    for iteration in range(1, n + 1):
        # Compute t_i and b_i
        t = [digit // 2 for digit in current_digits]
        b = [(digit / 2 - t[i]) * 10 for i, digit in enumerate(current_digits)]

        # Add t_i and b_i nodes (left to right)
        for idx in range(d):
            t_node_id = f"iter{iteration}_t{idx}"
            b_node_id = f"iter{iteration}_b{idx}"
            G.add_node(t_node_id, layer=iteration * 2, label=str(t[idx]), pos=(idx, -iteration * 2))
            G.add_node(b_node_id, layer=iteration * 2, label=str(int(round(b[idx]))), pos=(idx + 0.5, -iteration * 2))
            G.add_edge(f"iter{iteration - 1}_digit{idx}", t_node_id)
            G.add_edge(f"iter{iteration - 1}_digit{idx}", b_node_id)

        # Compute new digits
        new_digits = []
        new_digits.append(t[0])  # c0 = t1
        for i in range(1, d):
            new_digits.append(b[i - 1] + t[i])  # c_i = b_i + t_{i+1}
        new_digits.append(b[-1])  # c_d = b_d

        # Add new digits nodes (left to right)
        for idx, digit in enumerate(new_digits):
            new_node_id = f"iter{iteration}_digit{idx}"
            G.add_node(new_node_id, layer=iteration * 2 + 1, label=str(int(round(digit))),
                       pos=(idx, -iteration * 2 - 1))
            if idx == 0:
                G.add_edge(f"iter{iteration}_t{0}", new_node_id)
            elif idx == len(new_digits) - 1:
                G.add_edge(f"iter{iteration}_b{idx - 1}", new_node_id)
            else:
                G.add_edge(f"iter{iteration}_b{idx - 1}", new_node_id)
                G.add_edge(f"iter{iteration}_t{idx}", new_node_id)

        # Update current digits and d for next iteration
        current_digits = [int(round(digit)) for digit in new_digits]
        d = len(current_digits)

    # Extract positions and labels for drawing
    pos = {node: data['pos'] for node, data in G.nodes(data=True) if 'pos' in data}
    labels = {node: data['label'] for node, data in G.nodes(data=True) if 'label' in data}

    # Group nodes by their y-coordinate and sort them by x-coordinate
    layers = {}
    for node, (x, y) in pos.items():
        if y not in layers:
            layers[y] = []
        layers[y].append((x, labels[node]))

    # Sort each layer and collect rows
    rows = []
    for y in sorted(layers.keys(), reverse=True):  # Layers are drawn from top to bottom
        layer = layers[y]
        layer_sorted = sorted(layer, key=lambda x: x[0])
        row = [label for x, label in layer_sorted]
        rows.append(row)

    # Print each row separately
    for row in rows:
        print(' '.join(row))

    # Return the graph object for further use
    return G


# Example usage
if __name__ == "__main__":
    N = int(input("Enter a natural number N: "))
    n = int(input("Enter the number of iterations n: "))
    G = draw_digit_transformation_graph(N, n)  # Generate the graph and get the graph object