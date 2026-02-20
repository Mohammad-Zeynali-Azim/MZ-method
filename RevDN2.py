import networkx as nx
import matplotlib.pyplot as plt


# تابع رسم گراف تقسیم بر دو
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

    # Return the graph object for further use
    return G


# تابع معکوس تقسیم بر دو
def revers(x, n, result):
    y = []
    z = []

    y.clear()
    z.clear()

    y.append(x[0])
    for i in range(1, len(x) - 1):
        if x[i] < 5:
            l = 0.0
            r = x[i]
        else:
            l = 5.0
            r = x[i] - 5
        y.append(int(l))
        y.append(int(r))

    y.append(int(x[i + 1]))
    result.append(y)  # اضافه کردن y به result
    print("y:", y)

    for j in range(0, len(y), 2):
        z.append(int(2 * y[j] + 2 * y[j + 1] / 10))

    print("z:", z)
    result.append(z)  # اضافه کردن z به result

    n = n - 1
    if n > 0:
        return revers(z, n, result)  # بازگشت به تابع و ارسال result
    else:
        return result  # بازگشت نتیجه نهایی


# تابع تشخیص و اصلاح خطا
def detect_and_correct_error(N, n):
    # Step 1: Apply division by two algorithm
    G = draw_digit_transformation_graph(N, n)

    # Check if G is a graph object
    if not isinstance(G, nx.DiGraph):
        raise ValueError("The returned object is not a graph. Please check the function.")

    # Step 2: Extract the final digits from the graph
    final_digits = []
    for node, data in G.nodes(data=True):
        if data['layer'] == n * 2 + 1:  # Last layer
            final_digits.append(int(data['label']))

    # Step 3: Apply reverse algorithm
    result = []
    revers(final_digits, n, result)

    # Step 4: Compare and detect error
    original_number = [int(d) for d in str(N)]
    reconstructed_number = result[-1]  # Last element in result is the reconstructed number

    if original_number == reconstructed_number:
        print("No error detected. The process is correct.")
    else:
        print("Error detected! Original number:", original_number)
        print("Reconstructed number:", reconstructed_number)

        # Step 5: Correct the error
        print("Correcting the error...")
        # Here you can add logic to identify and correct the error
        # For example, you can compare intermediate steps and find where the error occurred.


# اجرای برنامه
if __name__ == "__main__":
    N = int(input("Enter a natural number N: "))
    n = int(input("Enter the number of iterations n: "))
    detect_and_correct_error(N, n)