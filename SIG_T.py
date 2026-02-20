#Similarity-Driven Division by Two Graph Complex Networ or SiCNet---With the Saving in Excel File
import MG9846 as mg
#import numpy as np
#import pylab as plt
import networkx as nx
#import random
#import collections
#import pandas as pd
#from docx import Document
#from io import BytesIO
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from sklearn.mixture import GaussianMixture
#from statsmodels.distributions.empirical_distribution import ECDF
#from scipy.optimize import curve_fit
#import community  # Import the community library
#import matplotlib.cm as cm  # Import the colormap module

# Create a Word file

def generate_random_numbers():
    n_digits = random.randint(1, 6)  # n between 10 and 999999
    n = random.randint(10**(n_digits-1), 10**n_digits - 1)
    m_digits = n_digits
    m = random.randint(10**(m_digits-1), 10**m_digits - 1)
    print(n,m)
    return n, m

def create_graph(n, m):
    num1 = [int(d) for d in str(n)]
    L1 = mg.Graph_Generate(num1, 200)
    mg.After_constructing(L1)

    natije1 = []
    for j in range(1, 200):
        L3 = mg.Dimond_value(j)
        if any(x != 0 for x in L3):
             natije1.append(L3)

    num2 = [int(d) for d in str(m)]
    L2 = mg.Graph_Generate(num2, 100)
    mg.After_constructing(L2)

    natije2 = []
    for j in range(1, 100):
        L4 = mg.Dimond_value(j)
        natije2.append(L4)
    list_for_Cyto1=[]
    list_for_Cyto2=[]
    G = nx.Graph()
    k=0
    l=0
    for k in range(len(natije1)):
        for l in range(len(natije2)):
            if natije1[k] == natije2[l]:
                G.add_edge(k, l)
                list_for_Cyto1.append(k)
                list_for_Cyto2.append(l)
    return G, list_for_Cyto1, list_for_Cyto2

#n, m = generate_random_numbers()
#print(n,m)
G, list_for_Cyto1, list_for_Cyto2 = create_graph(1381,81275369)
print(G.edges)
def Animate_Graph(G):
    import pygame
    import networkx as nx
    import time

    # ============ تنظیمات جدید ============
    WIDTH, HEIGHT = 1550, 900  # اندازه جدید
    NODE_RADIUS = 1
    NODE_COLOR = (100, 150, 255)
    EDGE_COLOR = (200, 200, 200)
    NEW_EDGE_COLOR = (255, 50, 50)
    BACKGROUND = (20, 20, 30)
    TEXT_COLOR = (255, 255, 255)
    AUTO_SPEED = 1.0  # ثانیه بین هر یال
    # =======================================

    # ایجاد شبکه
    edges = list(G.edges())
    pos = nx.spring_layout(G, k=0.4, iterations=50)

    # تنظیم موقعیت‌ها برای صفحه جدید
    for node in pos:
        pos[node] = (
            int((pos[node][0] + 1) * (WIDTH - 200) / 2 + 100),
            int((pos[node][1] + 1) * (HEIGHT - 200) / 2 + 100)
        )

    # مقداردهی pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Network Growth Animation DN2 method World")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 28)
    title_font = pygame.font.SysFont('Arial', 28, bold=True)  # فونت برای عنوان اصلی

    # متغیرها
    drawn_edges = []
    current_edge = 0
    mode = "manual"
    last_edge_time = 0
    running = True
    paused = False

    print("Controls:")
    print("SPACE: Add next edge manually")
    print("A: Start auto mode (1 sec per edge)")
    print("P: Pause/Resume auto mode")
    print("R: Reset animation")
    print("ESC: Exit")

    # حلقه اصلی
    while running:
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE and mode == "manual":
                    if current_edge < len(edges):
                        drawn_edges.append(edges[current_edge])
                        current_edge += 1

                elif event.key == pygame.K_a:  # شروع auto mode
                    mode = "auto"
                    paused = False
                    print("Auto mode started!")

                elif event.key == pygame.K_p and mode == "auto":  # pause/resume
                    paused = not paused
                    print("Paused" if paused else "Resumed")

                elif event.key == pygame.K_r:  # reset
                    drawn_edges = []
                    current_edge = 0
                    mode = "manual"
                    paused = False

        # Auto mode logic
        if mode == "auto" and not paused:
            if current_edge < len(edges):
                if current_time - last_edge_time >= AUTO_SPEED:
                    drawn_edges.append(edges[current_edge])
                    current_edge += 1
                    last_edge_time = current_time

        # ========== رسم صفحه ==========
        # پاک کردن صفحه
        screen.fill(BACKGROUND)

        # ========== اضافه کردن این بخش: عنوان اصلی ==========
        # متن "MZ-method World" با رنگ سبز و بزرگ
        title_text = title_font.render("DN2 Method World: MS-Pairs Based Complex Network Generation", True, (0, 255, 0))  # سبز
        title_rect = title_text.get_rect(center=(WIDTH // 2, 50))  # بالای صفحه و وسط
        screen.blit(title_text, title_rect)

        # خط زیر عنوان
        pygame.draw.line(screen, (0, 200, 0),
                         (WIDTH // 2 - 200, 90),
                         (WIDTH // 2 + 200, 90),
                         3)
        # ===================================================

        # رسم یال‌های قبلی (خاکستری)
        for u, v in drawn_edges[:-1]:  # همه بجز آخرین
            pygame.draw.line(screen, EDGE_COLOR,
                             pos[u], pos[v], 2)

        # رسم آخرین یال (قرمز)
        if drawn_edges:
            u, v = drawn_edges[-1]
            pygame.draw.line(screen, NEW_EDGE_COLOR,
                             pos[u], pos[v], 4)

        # رسم گره‌ها
        for node in G.nodes():
            pygame.draw.circle(screen, NODE_COLOR,
                               pos[node], NODE_RADIUS)
            pygame.draw.circle(screen, (255, 255, 255),
                               pos[node], NODE_RADIUS, 2)

        # ========== نمایش اطلاعات در سمت چپ ==========
        info_lines = [
            f"Nodes: {G.number_of_nodes()}",
            f"Edges: {len(drawn_edges)}/{len(edges)}",
            f"Mode: {mode.upper()} {'(PAUSED)' if paused else ''}",
        ]

        if drawn_edges:
            current = drawn_edges[-1]
            info_lines.append(f"Current Edge: ({current[0]}, {current[1]})")

        for i, line in enumerate(info_lines):
            text = font.render(line, True, TEXT_COLOR)
            screen.blit(text, (20, 120 + i * 35))  # پایین‌تر از عنوان

        # ========== راهنما در سمت راست ==========
        help_text = [
            "CONTROLS:",
            "SPACE: Manual add",
            "A: Auto mode",
            "P: Pause/Resume",
            "R: Reset",
            "ESC: Exit"
        ]

        for i, line in enumerate(help_text):
            color = (0, 200, 255) if i == 0 else (200, 200, 200)  # عنوان آبی
            text = font.render(line, True, color)
            screen.blit(text, (WIDTH - 250, 120 + i * 35))

        # ========== Progress bar ==========
        if len(edges) > 0:
            progress = len(drawn_edges) / len(edges)
            bar_width = 400  # عریض‌تر برای صفحه بزرگ
            bar_height = 25
            bar_x = WIDTH // 2 - bar_width // 2
            bar_y = HEIGHT - 80  # پایین‌تر

            # Background bar
            pygame.draw.rect(screen, (50, 50, 50),
                             (bar_x, bar_y, bar_width, bar_height),
                             border_radius=10)

            # Progress fill
            fill_width = int(bar_width * progress)
            pygame.draw.rect(screen, (0, 200, 100),
                             (bar_x, bar_y, fill_width, bar_height),
                             border_radius=10)

            # Progress text
            percent_text = f"{progress * 100:.1f}% Complete"
            percent = font.render(percent_text, True, (255, 255, 255))
            screen.blit(percent, (bar_x + bar_width // 2 - 70, bar_y - 35))

        # ========== Footer text ==========
        footer = font.render("Network Visualization", True, (150, 150, 200))
        screen.blit(footer, (WIDTH // 2 - 180, HEIGHT - 30))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("Animation finished!")
Animate_Graph(G)
