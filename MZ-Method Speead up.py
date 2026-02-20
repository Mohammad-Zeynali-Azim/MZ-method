import pygame
import sys
import time
import numpy as np
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Fundamental Theory of Division by Two(DN2/MZ-Method) Benchmark")
clock = pygame.time.Clock()

# Colors
BG = (8, 8, 18)
WHITE = (235, 235, 245)
GRAY = (65, 65, 95)
DARK = (22, 22, 38)
GREEN = (55, 195, 105)
YELLOW = (225, 190, 55)
BLUE = (55, 125, 245)
RED = (215, 55, 55)
CYAN = (55, 215, 215)

# Fonts
font = pygame.font.SysFont("consolas", 26)
font_small = pygame.font.SysFont("consolas", 22)
font_title = pygame.font.SysFont("consolas", 42, bold=True)
font_input = pygame.font.SysFont("consolas", 36, bold=True)

# State
#zeros_str = "9999999"
input_number = '1'# + '0' *( int(zeros_str)/10)
input_length = len(input_number)

input_active = False
single_results = ["", "", ""]
single_times = ["", "", ""]
compare_rows = []

PAGE_MAIN = 0
PAGE_COMPARE = 1
current_page = PAGE_MAIN


def update_input():
    global input_number, input_length
    try:
        count = int(zeros_str)
        if count < 0: count = 0
        input_number = '1' + '0' * count
        input_length = len(input_number)
        single_results[:] = ["", "", ""]
        single_times[:] = ["", "", ""]
    except ValueError:
        pass


# Algorithms
def vectorized(s):
    arr = np.frombuffer(s.encode(), dtype=np.uint8) - 48
    first_digit = arr[0] >> 1
    if len(arr) < 2:
        return []
    prev_parity = arr[:-1] & 1
    if first_digit > 0:
        return np.concatenate(([first_digit], (prev_parity * 5 + (arr[1:] >> 1)).tolist())).tolist()
    else:
        return (prev_parity * 5 + (arr[1:] >> 1)).tolist()


def vectorized_fast(arr, length):
    if length < 2:
        return 0
    prev_parity = arr[:-1] & 1
    arr[1:length] = (prev_parity * 5) + (arr[1:] >> 1)
    first = arr[0] >> 1
    if first > 0:
        arr[0] = first
        return length
    else:
        arr[:length-1] = arr[1:length]
        return length - 1


def div2_carry_numpy(s: str) -> str:
    if not s or s == '0':
        return '0'
    arr = np.frombuffer(s.encode('ascii'), dtype=np.uint8) - 48
    n = len(arr)
    result = np.zeros(n, dtype=np.uint8)
    carry = 0
    for i in range(n):
        current = carry * 10 + arr[i]
        result[i] = current >> 1
        carry = current & 1
    first = np.argmax(result != 0)
    if first == 0 and result[0] == 0:
        return '0'
    return ''.join(map(str, result[first:]))


# Drawing
def draw_rounded_rect(rect, color, radius=16):
    pygame.draw.rect(screen, color, rect, border_radius=radius)


def draw_button(x, y, w, h, text, base=GRAY, hover=GREEN):
    mouse = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]
    rect = pygame.Rect(x, y, w, h)
    col = hover if rect.collidepoint(mouse) else base
    draw_rounded_rect(rect, col)
    txt = font.render(text, True, WHITE)
    screen.blit(txt, (x + (w - txt.get_width())//2, y + (h - txt.get_height())//2))
    return rect.collidepoint(mouse) and clicked


def draw_zeros_input():
    rect = pygame.Rect(60, 60, WIDTH-120, 90)
    border_color = BLUE if input_active else GRAY

    pygame.draw.rect(screen, border_color, rect, width=4, border_radius=16)
    draw_rounded_rect(rect, DARK)

    label = font_small.render("Number of zeros after '1':", True, YELLOW)
    screen.blit(label, (rect.x + 30, rect.y + 8))

    cursor = "|" if input_active and (pygame.time.get_ticks() // 500) % 2 == 0 else ""
    text_surf = font_input.render(zeros_str + cursor, True, WHITE)
    screen.blit(text_surf, (rect.x + 30, rect.y + 38))

    len_text = font_small.render(f"Total digits: {input_length:,}", True, CYAN)
    screen.blit(len_text, (rect.x + 30, rect.y + 68))


def draw_single_results():
    if not any(single_results):
        return
    py = 420
    panel = pygame.Rect(60, py, WIDTH-120, 280)
    draw_rounded_rect(panel, DARK)
    pygame.draw.rect(screen, GRAY, panel, width=2, border_radius=16)

    title = font.render("Single Method Results", True, YELLOW)
    screen.blit(title, (panel.x + 30, panel.y + 20))

    y = panel.y + 80
    labels = ["MZ-List", "MZ-Array", "Div2-Carry"]
    for lbl, res, t in zip(labels, single_results, single_times):
        if not res: continue
        color = GREEN if "Error" not in res else RED
        name_surf = font_small.render(f"{lbl}:", True, WHITE)
        screen.blit(name_surf, (panel.x + 40, y))
        time_surf = font_small.render(f"time: {t} ms" if t else "", True, WHITE)
        screen.blit(time_surf, (panel.right - 280, y))
        res_surf = font_small.render(res, True, color)
        screen.blit(res_surf, (panel.x + 180, y))
        y += 60


def draw_compare_page():
    screen.fill(BG)

    title = font_title.render("Speedup Comparison", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))

    if not compare_rows:
        msg = font_small.render("No comparison data yet.", True, GRAY)
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 20))
    else:
        panel = pygame.Rect(60, 140, WIDTH-120, HEIGHT-280)
        draw_rounded_rect(panel, DARK)
        pygame.draw.rect(screen, GRAY, panel, width=2, border_radius=16)

        headers = ["Method", "Length", "Time (ms)", "MZ-Array Speedup"]
        x_pos = [panel.x + 60, panel.x + 340, panel.x + 620, panel.x + 880]

        for i, h in enumerate(headers):
            surf = font.render(h, True, YELLOW)
            screen.blit(surf, (x_pos[i], panel.y + 30))

        pygame.draw.line(screen, GRAY, (panel.x + 40, panel.y + 80),
                         (panel.right - 40, panel.y + 80), 2)

        y = panel.y + 100
        for row in compare_rows:
            for i, val in enumerate(row):
                if i == 3 and isinstance(val, (int, float)) and val > 0:
                    color = CYAN if val >= 2 else WHITE
                    txt_str = f"{val:.1f}× faster" if val >= 1 else f"{1/val:.1f}× slower"
                    txt = font_small.render(txt_str, True, color)
                else:
                    color = RED if val == "Error" else WHITE
                    txt = font_small.render(str(val), True, color)
                screen.blit(txt, (x_pos[i], y))
            y += 45

    hint = font_small.render("ESC to quit  •  SPACE or click to return", True, GRAY)
    screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 60))


def draw_presented_by():
    if current_page != PAGE_MAIN or any(single_results):
        return

    rect = pygame.Rect(40, HEIGHT - 320, 520, 280)
    draw_rounded_rect(rect, DARK)
    pygame.draw.rect(screen, (45, 45, 85), rect, width=4, border_radius=18)

    lines = [
        "Presented by",
        "Dr. Babak Anari",
        "Dr. Saeid Alikhani",
        "Dr. Bagher Zarei",
        "Mohammad Zeynali Azim"
    ]
    y = rect.y + 35
    for i, line in enumerate(lines):
        color = YELLOW if i == 0 else (190, 225, 255)
        txt = font_small.render(line, True, color)
        screen.blit(txt, (rect.x + 40, y))
        y += 48


# ─── Main loop ───
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if current_page == PAGE_MAIN:
                if event.key == pygame.K_RETURN:
                    if input_active:
                        update_input()
                        input_active = False

                elif input_active:
                    if event.key == pygame.K_BACKSPACE:
                        zeros_str = zeros_str[:-1]
                    elif event.unicode.isdigit():
                        zeros_str += event.unicode
                    if len(zeros_str) > 10:
                        zeros_str = zeros_str[:10]

            if current_page == PAGE_COMPARE:
                if event.key == pygame.K_SPACE:
                    current_page = PAGE_MAIN
                    single_results = ["", "", ""]
                    single_times = ["", "", ""]

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            input_rect = pygame.Rect(60, 60, WIDTH-120, 90)
            input_active = input_rect.collidepoint(mouse_pos)

            if current_page == PAGE_COMPARE:
                current_page = PAGE_MAIN
                single_results = ["", "", ""]
                single_times = ["", "", ""]

    screen.fill(BG)

    if current_page == PAGE_MAIN:
        title_surf = font_title.render("Fundamental Theory of Division by Two(DN2) Benchmark", True, WHITE)
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 10))

        draw_zeros_input()   # ← اینجا فراخوانی درست است

        btn_y = 170
        clicked1 = draw_button(100, btn_y, 320, 75, "Run MZ-List")
        clicked2 = draw_button(WIDTH//2 - 160, btn_y, 320, 75, "Run MZ-Array")
        clicked3 = draw_button(WIDTH - 420, btn_y, 320, 75, "Run Div2-Carry")

        compare_clicked = draw_button(WIDTH//2 - 240, 270, 480, 75, "Compare + Speedup", YELLOW)


        if clicked1:
            t0 = time.perf_counter_ns()
            res = vectorized(input_number)
            ms = (time.perf_counter_ns() - t0) / 1_000_000
            single_results[0] = f"list, len = {len(res)}"
            single_times[0] = f"{ms:.3f}"

        if clicked2:
            t0 = time.perf_counter_ns()
            arr = np.frombuffer(input_number.encode(), dtype=np.uint8) - 48
            length = len(arr)
            new_len = vectorized_fast(arr, length)
            ms = (time.perf_counter_ns() - t0) / 1_000_000
            single_results[1] = f"array, effective len = {new_len}"
            single_times[1] = f"{ms:.3f}"

        if clicked3:
            t0 = time.perf_counter_ns()
            res = div2_carry_numpy(input_number)
            ms = (time.perf_counter_ns() - t0) / 1_000_000
            single_results[2] = f"string, len = {len(res)}"
            single_times[2] = f"{ms:.3f}"

        if compare_clicked:
            times = [None] * 3
            compare_rows = []

            t0 = time.perf_counter_ns()
            res = vectorized(input_number)
            times[0] = (time.perf_counter_ns() - t0) / 1_000_000
            compare_rows.append(["MZ-List", f"{len(res):,}", f"{times[0]:.3f}", 0.0])

            t0 = time.perf_counter_ns()
            arr = np.frombuffer(input_number.encode(), dtype=np.uint8) - 48
            length = len(arr)
            new_len = vectorized_fast(arr, length)
            times[1] = (time.perf_counter_ns() - t0) / 1_000_000
            compare_rows.append(["MZ-Array", f"{new_len:,}", f"{times[1]:.3f}", 0.0])

            t0 = time.perf_counter_ns()
            res = div2_carry_numpy(input_number)
            times[2] = (time.perf_counter_ns() - t0) / 1_000_000
            compare_rows.append(["Div2-Carry", f"{len(res):,}", f"{times[2]:.3f}", 0.0])

            mz_array_time = times[1] if times[1] is not None else 1.0
            for i, row in enumerate(compare_rows):
                row[3] = round(times[i] / mz_array_time, 2) if mz_array_time > 0 else 0

            current_page = PAGE_COMPARE

        draw_single_results()
        draw_presented_by()

        hint = font_small.render("ESC to quit  •  Click box to change zero count", True, GRAY)
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 60))

    else:
        draw_compare_page()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()