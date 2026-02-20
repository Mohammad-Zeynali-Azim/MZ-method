import pandas as pd
import networkx as nx

# Read the Excel file
df = pd.read_excel('6009.xlsx')

# Build the undirected graph
G = nx.Graph()  # تغییر از DiGraph به Graph
for index, row in df.iterrows():
    G.add_edge(int(row['A']), int(row['B']))  # گراف غیرجهت‌دار به طور خودکار هر یال را دوطرفه اضافه می‌کند


def generate_random_number(G, step):
    # Determine the starting node based on the step (e.g., modulo the number of nodes)
    start_node = list(G.nodes())[step % len(G.nodes())]
    current_node = start_node
    binary_string = ""

    # Traverse the graph (e.g., 100 steps)
    for i in range(100):
        # Append the current node ID to the binary string
        binary_string += str(current_node)

        # Move to the next node based on a dynamic rule
        neighbors = list(G.neighbors(current_node))  # تغییر به neighbors برای گراف غیرجهت‌دار
        if neighbors:
            # Choose the next node based on a dynamic rule (e.g., step modulo number of neighbors)
            next_node = neighbors[(step + i) % len(neighbors)]
        else:
            # If no neighbors, jump to a random node (based on the step)
            next_node = list(G.nodes())[(step + i) % len(G.nodes())]

        current_node = next_node

    # Convert the binary string to a numerical value
    random_number = int(binary_string) % (1 << 32)  # Modulo to limit the range
    random_number = random_number / (1 << 32)  # Normalize to [0, 1)

    return random_number


print("shrou")
# Generate 10,000 binary random numbers (0s and 1s)
binary_random_numbers = []
for step in range(1000000):
    # Generate a random number in [0, 1)
    random_number = generate_random_number(G, step)

    # Extract a single bit (e.g., the least significant bit)
    binary_bit = int(random_number * 2) % 2  # Multiply by 2 and take modulo 2
    binary_random_numbers.append(binary_bit)
# Save the binary random numbers to a file
with open('60009.txt', 'w') as f:
    for bit in binary_random_numbers:
        f.write(f"{bit}")
print("Tamam")
