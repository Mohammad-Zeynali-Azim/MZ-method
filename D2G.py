import pygame
import networkx as nx
import math

# ============ تنظیمات Pygame ============
WIDTH, HEIGHT = 1500, 900
BACKGROUND = (15, 20, 30)
NODE_COLOR = (80, 180, 255)
EDGE_COLOR = (120, 120, 200)
TEXT_COLOR = (255, 255, 255)
LAYER_COLORS = [
    (255, 100, 100),  # لایه 0 - قرمز
    (100, 255, 100),  # لایه 1 - سبز
    (100, 100, 255),  # لایه 2 - آبی
    (255, 255, 100),  # لایه 3 - زرد
    (255, 100, 255),  # لایه 4 - بنفش
    (100, 255, 255),  # لایه 5 - فیروزه‌ای
]


# ============ تابع ایجاد گراف ============
def create_digit_transformation_graph(N, n):
    G = nx.DiGraph()
    current_digits = [int(d) for d in str(N)]
    d = len(current_digits)

    # افزودن ارقام اولیه
    for idx, digit in enumerate(current_digits):
        node_id = f"iter0_digit{idx}"
        G.add_node(node_id, layer=0, label=str(digit),
                   type='digit', iteration=0, index=idx)

    for iteration in range(1, n + 1):
        # محاسبه t_i و b_i
        t = [digit // 2 for digit in current_digits]
        b = [(digit / 2 - t[i]) * 10 for i, digit in enumerate(current_digits)]

        # افزودن گره‌های t_i و b_i
        for idx in range(d):
            t_node_id = f"iter{iteration}_t{idx}"
            b_node_id = f"iter{iteration}_b{idx}"
            G.add_node(t_node_id, layer=iteration * 2 - 1, label=f"{t[idx]}",
                       type='t', iteration=iteration, index=idx)
            G.add_node(b_node_id, layer=iteration * 2 - 1, label=f"{b[idx]}",
                       type='b', iteration=iteration, index=idx)

            # اتصال از رقم قبلی به t و b
            G.add_edge(f"iter{iteration - 1}_digit{idx}", t_node_id)
            G.add_edge(f"iter{iteration - 1}_digit{idx}", b_node_id)

        # محاسبه ارقام جدید
        new_digits = []
        new_digits.append(t[0])  # c0 = t1
        for i in range(1, d):
            new_digits.append(b[i - 1] + t[i])  # c_i = b_i + t_{i+1}
        new_digits.append(b[-1])  # c_d = b_d

        # افزودن گره‌های ارقام جدید
        for idx, digit in enumerate(new_digits):
            new_node_id = f"iter{iteration}_digit{idx}"
            G.add_node(new_node_id, layer=iteration * 2, label=str(int(round(digit))),
                       type='digit', iteration=iteration, index=idx)

            # اتصال‌ها
            if idx == 0:
                G.add_edge(f"iter{iteration}_t{0}", new_node_id)
            elif idx == len(new_digits) - 1:
                G.add_edge(f"iter{iteration}_b{idx - 1}", new_node_id)
            else:
                G.add_edge(f"iter{iteration}_b{idx - 1}", new_node_id)
                G.add_edge(f"iter{iteration}_t{idx}", new_node_id)

        # به‌روزرسانی ارقام برای تکرار بعدی
        current_digits = [int(round(digit)) for digit in new_digits]
        d = len(current_digits)

    return G


# ============ تابع محاسبه موقعیت‌ها ============
def calculate_positions(G):
    pos = {}
    max_layers = max(data['layer'] for _, data in G.nodes(data=True))

    for node, data in G.nodes(data=True):
        layer = data['layer']
        idx = data.get('index', 0)
        node_type = data.get('type', 'digit')
        iteration = data.get('iteration', 0)

        # موقعیت افقی بر اساس ایندکس
        x_spacing = WIDTH / (max(G.nodes(data='index'), key=lambda x: x[1] if x[1] is not None else 0)[1] + 4)
        x = 200 + idx * x_spacing

        # موقعیت عمودی بر اساس لایه
        y_spacing = HEIGHT / (max_layers + 3)
        y = 150 + layer * y_spacing

        # تنظیم دقیق‌تر بر اساس نوع گره
        if node_type == 't':
            x -= x_spacing * 0.25
        elif node_type == 'b':
            x += x_spacing * 0.25

        pos[node] = (x, y)

    return pos

print("Digit Transformation Graph Visualization")
print("=" * 50)
N = int(input("Enter a natural number N: "))
n = int(input("Enter the number of iterations n: "))
# ============ Pygame Setup ============
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MZ-method- Division Graph by Two(D2G)")
clock = pygame.time.Clock()

# فونت‌ها
title_font = pygame.font.SysFont('Arial', 35, bold=True)
node_font = pygame.font.SysFont('Arial', 20)
info_font = pygame.font.SysFont('Arial', 28)
layer_font = pygame.font.SysFont('Arial', 24, bold=True)

# ============ دریافت ورودی ============


# ایجاد گراف
print(f"\nCreating graph for N={N}, n={n}...")
G = create_digit_transformation_graph(N, n)
pos = calculate_positions(G)

print(f"Graph created: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# ============ متغیرهای انیمیشن ============
current_layer = 0
max_layer = max(data['layer'] for _, data in G.nodes(data=True))
auto_mode = False
show_labels = True
running = True
animation_speed = 1.0  # ثانیه بین هر لایه

print("\nControls:")
print("SPACE: Toggle Auto/Manual mode")
print("RIGHT/LEFT: Next/Previous layer")
print("L: Toggle labels")
print("R: Reset animation")
print("ESC: Exit")

# ============ حلقه اصلی ============
last_layer_time = 0
while running:
    current_time = pygame.time.get_ticks() / 1000.0

    # پردازش رویدادها
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                auto_mode = not auto_mode
                print(f"Auto mode: {'ON' if auto_mode else 'OFF'}")
            elif event.key == pygame.K_RIGHT:
                if current_layer < max_layer:
                    current_layer += 1
                    print(f"Showing layer {current_layer}")
            elif event.key == pygame.K_LEFT:
                if current_layer > 0:
                    current_layer -= 1
                    print(f"Showing layer {current_layer}")
            elif event.key == pygame.K_l:
                show_labels = not show_labels
                print(f"Labels: {'ON' if show_labels else 'OFF'}")
            elif event.key == pygame.K_r:
                current_layer = 0
                auto_mode = False
                print("Reset to layer 0")

    # حالت اتوماتیک
    if auto_mode and current_time - last_layer_time > animation_speed:
        if current_layer < max_layer:
            current_layer += 1
            last_layer_time = current_time
            print(f"Auto: Showing layer {current_layer}")
        else:
            auto_mode = False
            print("Auto mode finished")

    # ============ رسم صفحه ============
    screen.fill(BACKGROUND)

    # عنوان
    title = title_font.render(f"Digit Transformation Graph: N={N}, Iterations={n}",
                              True, (0, 255, 100))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    # ============ رسم لایه‌ها ============
    # محاسبه گره‌ها و یال‌های قابل نمایش تا لایه فعلی
    visible_nodes = [node for node, data in G.nodes(data=True)
                     if data['layer'] <= current_layer]
    visible_edges = [edge for edge in G.edges()
                     if edge[0] in visible_nodes and edge[1] in visible_nodes]

    # رسم یال‌ها
    for u, v in visible_edges:
        if u in pos and v in pos:
            # رنگ یال بر اساس لایه مبدأ
            source_layer = G.nodes[u]['layer']
            color_idx = min(source_layer, len(LAYER_COLORS) - 1)
            edge_color = LAYER_COLORS[color_idx]

            pygame.draw.line(screen, edge_color, pos[u], pos[v], 2)

            # فلش برای گراف جهت‌دار
            dx = pos[v][0] - pos[u][0]
            dy = pos[v][1] - pos[u][1]
            length = math.sqrt(dx * dx + dy * dy)
            if length > 0:
                dx, dy = dx / length, dy / length
                arrow_size = 10
                pygame.draw.polygon(screen, edge_color, [
                    pos[v],
                    (pos[v][0] - dx * arrow_size + dy * arrow_size / 2,
                     pos[v][1] - dy * arrow_size - dx * arrow_size / 2),
                    (pos[v][0] - dx * arrow_size - dy * arrow_size / 2,
                     pos[v][1] - dy * arrow_size + dx * arrow_size / 2)
                ])

    # رسم گره‌ها
    for node in visible_nodes:
        if node in pos:
            x, y = pos[node]
            node_data = G.nodes[node]
            layer = node_data['layer']

            # رنگ گره بر اساس لایه
            color_idx = min(layer, len(LAYER_COLORS) - 1)
            node_color = LAYER_COLORS[color_idx]

            # اندازه گره
            radius = 25 if node_data['type'] == 'digit' else 20

            # رسم گره
            pygame.draw.circle(screen, node_color, (int(x), int(y)), radius)
            pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), radius, 2)

            # نمایش لیبل
            if show_labels:
                label = node_data.get('label', '')
                text = node_font.render(label, True, (0, 0, 0))
                text_rect = text.get_rect(center=(int(x), int(y)))
                screen.blit(text, text_rect)

    # ============ پانل اطلاعات ============
    info_y = HEIGHT - 200

    # اطلاعات گراف
    info_lines = [
        f"Current Layer: {current_layer}/{max_layer}",
        f"Visible Nodes: {len(visible_nodes)}/{G.number_of_nodes()}",
        f"Visible Edges: {len(visible_edges)}/{G.number_of_edges()}",
        f"Mode: {'AUTO' if auto_mode else 'MANUAL'}",
        f"Speed: {animation_speed:.1f}s per layer",
    ]

    for i, line in enumerate(info_lines):
        text = info_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (30, info_y + i * 35))

    # راهنما
    help_lines = [
        "CONTROLS:",
        "SPACE: Toggle Auto/Manual",
        "→ : Next layer",
        "← : Previous layer",
        "L: Toggle labels",
        "R: Reset",
        "ESC: Exit"
    ]

    for i, line in enumerate(help_lines):
        color = (0, 200, 255) if i == 0 else (200, 200, 200)
        text = info_font.render(line, True, color)
        screen.blit(text, (WIDTH - 300, info_y + i * 35))

    # ============ Legend ============
    legend_y = 100
    legend_title = layer_font.render("Layer Legend:", True, (255, 255, 200))
    screen.blit(legend_title, (WIDTH - 350, legend_y))

    for i in range(min(max_layer + 1, 6)):
        color = LAYER_COLORS[i]
        layer_text = f"Layer {i}"
        text = info_font.render(layer_text, True, color)

        # نمونه رنگ
        pygame.draw.rect(screen, color, (WIDTH - 350, legend_y + 40 + i * 40, 30, 20))
        pygame.draw.rect(screen, (255, 255, 255), (WIDTH - 350, legend_y + 40 + i * 40, 30, 20), 1)

        screen.blit(text, (WIDTH - 310, legend_y + 40 + i * 40))

    # ============ Progress Bar ============
    if max_layer > 0:
        progress = current_layer / max_layer
        bar_width = 600
        bar_height = 20
        bar_x = WIDTH // 2 - bar_width // 2
        bar_y = HEIGHT - 50

        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 200, 100),
                         (bar_x, bar_y, int(bar_width * progress), bar_height))

        progress_text = info_font.render(f"Layer Progress: {progress * 100:.1f}%",
                                         True, TEXT_COLOR)
        screen.blit(progress_text, (bar_x + bar_width // 2 - 100, bar_y - 30))

    # ============ نمایش جزئیات لایه فعلی ============
    if current_layer > 0:
        layer_nodes = [node for node, data in G.nodes(data=True)
                       if data['layer'] == current_layer]
        layer_info = f"Layer {current_layer}: {len(layer_nodes)} nodes"
        layer_display = info_font.render(layer_info, True, (255, 255, 100))
        screen.blit(layer_display, (30, HEIGHT - 300))

        # نمایش انواع گره‌ها در این لایه
        types = {}
        for node in layer_nodes:
            node_type = G.nodes[node]['type']
            types[node_type] = types.get(node_type, 0) + 1

        type_y = HEIGHT - 260
        for i, (node_type, count) in enumerate(types.items()):
            type_text = f"{node_type}: {count}"
            text = info_font.render(type_text, True, (200, 200, 200))
            screen.blit(text, (30, type_y + i * 35))

    pygame.display.flip()
    clock.tick(60)

# ============ پایان ============
pygame.quit()
print("\nProgram finished!")
print(f"Graph statistics:")
print(f"- Total nodes: {G.number_of_nodes()}")
print(f"- Total edges: {G.number_of_edges()}")
print(f"- Maximum layer: {max_layer}")

# ذخیره اطلاعات
with open(f'digit_graph_N{N}_n{n}.txt', 'w') as f:
    f.write(f"Digit Transformation Graph: N={N}, Iterations={n}\n")
    f.write("=" * 50 + "\n")
    f.write(f"Total nodes: {G.number_of_nodes()}\n")
    f.write(f"Total edges: {G.number_of_edges()}\n\n")

    for layer in range(max_layer + 1):
        layer_nodes = [node for node, data in G.nodes(data=True)
                       if data['layer'] == layer]
        f.write(f"Layer {layer} ({len(layer_nodes)} nodes):\n")
        for node in layer_nodes:
            label = G.nodes[node].get('label', '')
            f.write(f"  {node}: {label}\n")
        f.write("\n")

print(f"Graph details saved to 'digit_graph_N{N}_n{n}.txt'")