import pygame
import networkx as nx
import pandas as pd
import os
import time
import math

# ============ تنظیمات ============
WIDTH, HEIGHT = 1560, 900
BACKGROUND = (15, 20, 30)
NODE_COLOR = (80, 140, 255)
EDGE_COLOR = (80, 80, 120)
TRAVERSAL_COLOR = (0, 255, 0)  # رنگ مسیر پیمایش
CURRENT_NODE_COLOR = (255, 50, 50)  # رنگ گره فعلی
TEXT_COLOR = (255, 255, 255)
# =================================

# ============ خواندن شبکه از فایل ============
print("Loading network from file...")
base_dir = r'C:\Users\WE'
file_name = '6002.xlsx'
file_path = os.path.join(base_dir, file_name)

df = pd.read_excel(file_path)
G = nx.Graph()

for index, row in df.iterrows():
    G.add_edge(int(row['A']), int(row['B']))

print(f"Network loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")


# =============================================

# ============ الگوریتم پیمایش ============
def generate_random_number(G, step, path_history):
    start_node = list(G.nodes())[step % len(G.nodes())]
    current_node = start_node
    binary_string = ""
    path = []  # مسیر پیمایش برای انیمیشن

    # 20 مرحله پیمایش
    for i in range(100):
        # ذخیره گره فعلی
        path.append(current_node)
        binary_string += str(current_node)

        # حرکت به گره بعدی
        neighbors = list(G.neighbors(current_node))
        if neighbors:
            next_node = neighbors[(step + i) % len(neighbors)]
        else:
            next_node = list(G.nodes())[(step + i) % len(G.nodes())]

        # ذخیره یال طی شده
        path.append((current_node, next_node))
        current_node = next_node

    path.append(current_node)  # آخرین گره
    path_history.append(path)  # ذخیره مسیر برای نمایش

    # تولید عدد تصادفی
    random_number = int(binary_string) % (1 << 32)
    random_number = random_number / (1 << 32)

    return random_number, path


# =========================================

# ============ Pygame Setup ============
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graph Traversal Animation - DN2-method")
clock = pygame.time.Clock()

# فونت‌ها
title_font = pygame.font.SysFont('Arial', 42, bold=True)
info_font = pygame.font.SysFont('Arial', 28)
number_font = pygame.font.SysFont('Consolas', 32, bold=True)

# محاسبه موقعیت‌ها
print("Calculating layout...")
pos = nx.spring_layout(G, k=0.5 / math.sqrt(G.number_of_nodes()),
                       iterations=100, seed=42)

# تنظیم موقعیت‌ها برای صفحه
for node in pos:
    pos[node] = (
        int((pos[node][0] + 1) * (WIDTH - 300) / 2 + 150),
        int((pos[node][1] + 1) * (HEIGHT - 300) / 2 + 150)
    )
# ======================================

# ============ متغیرهای انیمیشن ============
all_edges = list(G.edges())
path_history = []  # تاریخچه مسیرها
random_numbers = []  # اعداد تولید شده
current_step = 0
auto_mode = False
show_full_graph = True
traversal_speed = 0.3  # ثانیه بین هر مرحله پیمایش
running = True
# ========================================

print("\nControls:")
print("SPACE: Start/Stop auto traversal")
print("N: Next step manually")
print("R: Reset")
print("ESC: Exit")

# ============ حلقه اصلی ============
while running:
    current_time = time.time()

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
            elif event.key == pygame.K_n:  # مرحله بعدی دستی
                if current_step < 100:  # 100 مرحله پیمایش
                    random_num, path = generate_random_number(G, current_step, path_history)
                    random_numbers.append(random_num)
                    current_step += 1
                    print(f"Step {current_step}: Generated number = {random_num:.10f}")
            elif event.key == pygame.K_r:  # ریست
                path_history = []
                random_numbers = []
                current_step = 0
                print("Reset animation")

    # حالت اتوماتیک
    if auto_mode and current_step < 100:
        if len(path_history) == 0 or len(path_history[-1]) > 0:
            random_num, path = generate_random_number(G, current_step, path_history)
            random_numbers.append(random_num)
            current_step += 1
            print(f"Step {current_step}: Generated number = {random_num:.10f}")
            time.sleep(traversal_speed)  # توقف برای نمایش

    # ============ رسم صفحه ============
    screen.fill(BACKGROUND)

    # عنوان
    title = title_font.render("DN2 World: Complex Graph Traversal for Generating Pseudo Random Numbers", True, (0, 255, 0))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    # ============ رسم شبکه کامل ============
    # یال‌ها
    for u, v in all_edges:
        pygame.draw.line(screen, EDGE_COLOR, pos[u], pos[v], 1)

    # گره‌ها
    for node, (x, y) in pos.items():
        pygame.draw.circle(screen, NODE_COLOR, (x, y), 8)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 8, 1)

    # ============ نمایش مسیر پیمایش ============
    if path_history:
        current_path = path_history[-1]

        # نمایش یال‌های طی شده در این مرحله
        for i in range(0, len(current_path) - 2, 2):
            if i + 1 < len(current_path):
                edge_info = current_path[i + 1]
                if isinstance(edge_info, tuple) and len(edge_info) == 2:
                    u, v = edge_info
                    if u in pos and v in pos:
                        # رسم یال با رنگ سبز و ضخیم
                        pygame.draw.line(screen, TRAVERSAL_COLOR,
                                         pos[u], pos[v], 4)

        # نمایش گره‌های طی شده
        for i, node in enumerate(current_path):
            if isinstance(node, int) and node in pos:
                x, y = pos[node]
                # رنگ گره فعلی در پیمایش
                if i == len(current_path) - 1:  # آخرین گره
                    pygame.draw.circle(screen, CURRENT_NODE_COLOR, (x, y), 12)
                    pygame.draw.circle(screen, (255, 255, 255), (x, y), 12, 2)
                else:
                    pygame.draw.circle(screen, TRAVERSAL_COLOR, (x, y), 10)
                    pygame.draw.circle(screen, (255, 255, 255), (x, y), 10, 1)

    # ============ پانل اطلاعات ============
    # پانل سمت چپ
    info_y = 100
    info_lines = [
        f"Network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges",
        f"Traversal Step: {current_step}/100",
        f"Mode: {'AUTO' if auto_mode else 'MANUAL'}",
        f"Numbers Generated: {len(random_numbers)}",
    ]

    for i, line in enumerate(info_lines):
        text = info_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (30, info_y + i * 40))

    # نمایش آخرین عدد تولید شده
    if random_numbers:
        last_num = random_numbers[-1]
        num_text = f"Last Number: {last_num:.10f}"
        num_display = number_font.render(num_text, True, (255, 255, 100))
        screen.blit(num_display, (30, info_y + 180))

        # نمایش باینری (۸ بیت اول)
        binary_rep = ''.join(format(int(c), 'b') for c in str(last_num).replace('.', '')[:8])
        binary_text = f"Binary (first 8 bits): {binary_rep[:8]}"
        binary_display = info_font.render(binary_text, True, (100, 255, 255))
        screen.blit(binary_display, (30, info_y + 230))

    # ============ پانل راهنما ============
    help_y = 100
    help_lines = [
        "CONTROLS:",
        "SPACE: Toggle Auto/Manual",
        "N: Next step (manual)",
        "R: Reset animation",
        "ESC: Exit",
        "",
        "LEGEND:",
        "Blue: Regular nodes",
        "Green: Traversed path",
        "Red: Current node",
        "Gray: Network edges"
    ]

    for i, line in enumerate(help_lines):
        color = (0, 200, 255) if i == 0 else (100, 255, 100) if i == 6 else (200, 200, 200)
        text = info_font.render(line, True, color)
        screen.blit(text, (WIDTH - 350, help_y + i * 35))

    # ============ نمایش تاریخچه اعداد ============
    if random_numbers:
        history_title = info_font.render("Recent Numbers:", True, (255, 200, 100))
        screen.blit(history_title, (WIDTH // 2 - 200, HEIGHT - 180))

        # نمایش ۵ عدد آخر
        start_idx = max(0, len(random_numbers) - 5)
        for i, num in enumerate(random_numbers[start_idx:]):
            num_str = f"{start_idx + i + 1:3d}: {num:.8f}"
            num_text = info_font.render(num_str, True, (220, 220, 220))
            screen.blit(num_text, (WIDTH // 2 - 200, HEIGHT - 130 + i * 30))

    # ============ Progress Bar ============
    progress = current_step / 100
    bar_width = 600
    bar_height = 20
    bar_x = WIDTH // 2 - bar_width // 2
    bar_y = HEIGHT - 50

    pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, (0, 200, 100),
                     (bar_x, bar_y, int(bar_width * progress), bar_height))

    progress_text = info_font.render(f"Progress: {progress * 100:.1f}%", True, TEXT_COLOR)
    screen.blit(progress_text, (bar_x + bar_width // 2 - 60, bar_y - 30))

    pygame.display.flip()
    clock.tick(60)

# ============ پایان برنامه ============
pygame.quit()

# ذخیره نتایج
print("\nSaving results...")
if random_numbers:
    with open('generated_numbers.txt', 'w') as f:
        for i, num in enumerate(random_numbers):
            f.write(f"Step {i + 1}: {num:.10f}\n")

    with open('binary_output.txt', 'w') as f:
        for num in random_numbers:
            # تبدیل به باینری ۳۲ بیتی
            binary_value = ''.join(format(ord(c), '08b') for c in str(num))
            f.write(f"{binary_value[:32]}\n")

    print(f"Generated {len(random_numbers)} random numbers")
    print("Results saved to 'generated_numbers.txt' and 'binary_output.txt'")

print("Program finished!")