import pygame
import MG9846 as mg  # MZ-Method
import time

# =========================================== Cellular Automata Initialization =====================
print("=" * 120)
print("MZ-method Cellular Automata")
print("=" * 60)

n = int(input("Please enter initial value of cellular automata: "))
num1 = [int(d) for d in str(n)]

# Generate cellular automata using MZ-method (از کد شما)
L1 = mg.Graph_Generate(num1, 101)
list3 = []
for i in range(1, 101):
    l2 = mg.Node_value_in_Level(i, L1)
    list3.append(l2)

# Define colors (همانند کد شما)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
zero = (232, 239, 255)
one = (205, 231, 251)
two = (159, 209, 249)
three = (111, 186, 246)
four = (74, 168, 245)
five = (40, 153, 243)
six = (33, 138, 230)
seven = (21, 117, 209)
eight = (20, 97, 188)
nine = (51, 100, 175)

# ============ Pygame Setup ============
pygame.init()
WIDTH, HEIGHT = 1550, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MZ-method Cellular Automata")

# Fonts
title_font = pygame.font.SysFont('Arial', 42, bold=True)
info_font = pygame.font.SysFont('Arial', 28)
status_font = pygame.font.SysFont('Arial', 32, bold=True)
small_font = pygame.font.SysFont('Arial', 24)
digit_font = pygame.font.SysFont('Arial', 14, bold=True)
coord_font = pygame.font.SysFont('Arial', 18)

# ============ Settings ============
CELL_SIZE = 20  # اندازه سلول
MARGIN = 1
MAX_ROWS = 26  # تعداد سطرها: 41 (تغییر اصلی)
MAX_COLS = 63  # تعداد ستون‌ها: 60 (تغییر اصلی)

# محاسبه ابعاد صفحه شطرنج
CHESSBOARD_WIDTH = MAX_COLS * (CELL_SIZE + MARGIN)
CHESSBOARD_HEIGHT = MAX_ROWS * (CELL_SIZE + MARGIN)

# موقعیت مرکزی صفحه شطرنج (با فاصله بیشتر از عنوان)
chessboard_x = (WIDTH - CHESSBOARD_WIDTH) // 2
chessboard_y = 250  # فاصله بیشتر از نوشته‌ها (تغییر)

print(f"\nChessboard at center: ({chessboard_x}, {chessboard_y})")
print(f"Chessboard size: {CHESSBOARD_WIDTH}x{CHESSBOARD_HEIGHT}")

# ============ Create Lattice (از کد شما) ============
lattice = []
for row in range(MAX_ROWS):
    lattice.append([])
    for column in range(MAX_COLS):
        lattice[row].append(40)  # مقدار پیش‌فرض

# محاسبه موقعیت شروع برای مرکز کردن
center_col = MAX_COLS // 2
if len(num1) % 2 == 1:  # تعداد ارقام فرد
    start_col = center_col - (len(num1) // 2)+(len(num1) // 2)+1
else:  # تعداد ارقام زوج
    start_col = center_col - (len(num1) // 2) + (len(num1) // 2)+3

print(f"\nCenter calculation:")
print(f"Number: {n}, Digits: {num1}")
print(f"Center column: {center_col}")
print(f"Start column: {start_col}")
print(f"Middle digit '{num1[len(num1) // 2]}' will be at column {center_col}")

# پر کردن lattice طبق منطق کد شما
if (n < 10):
    y = 64 - (len(num1) // 2 * 4 - 1)
    ynew = 64 - (len(num1) // 2 * 4 - 1)
    roww = 0
    for p in list3[:MAX_ROWS]:  # فقط سطرهای قابل مشاهده
        if (roww == 0):
            ynew = 65 - (len(num1) // 2 * 4 - 1) - 2
        else:
            ynew = 65 - (len(num1) // 2 * 4 - 1) - roww - 3

        for k in p:
            # تطبیق موقعیت با صفحه شطرنج مرکزی
            adjusted_y = start_col + (ynew - 64)
            if 0 <= adjusted_y < MAX_COLS:
                lattice[roww][adjusted_y] = k

            if (roww % 2 == 0 and roww != 0):
                ynew = ynew + 2
            else:
                ynew = ynew + 4
        roww = roww + 1
else:
    y = 64 - (len(num1) // 2 * 4 - 1)
    ynew = 64 - (len(num1) // 2 * 4 - 1)
    roww = 0
    for p in list3[:MAX_ROWS]:  # فقط سطرهای قابل مشاهده
        ynew = 65 - (len(num1) // 2 * 4 - 1) - roww - 3

        for k in p:
            # تطبیق موقعیت با صفحه شطرنج مرکزی
            adjusted_y = start_col + (ynew - 64)
            if 0 <= adjusted_y < MAX_COLS:
                lattice[roww][adjusted_y] = k

            if (roww % 2 == 0):
                ynew = ynew + 4
            else:
                ynew = ynew + 2
        roww = roww + 1

# ============ Animation Variables ============
current_row = 0
total_rows = min(MAX_ROWS, len(list3))
auto_proceed = False
step_delay = 0.8
last_step_time = time.time()
show_numbers = True


# ============ Helper Functions ============
def get_color(value):
    """رنگ مربوط به هر مقدار را برمی‌گرداند (از کد شما)"""
    if value == 0:
        return zero
    elif value == 1:
        return one
    elif value == 2:
        return two
    elif value == 3:
        return three
    elif value == 4:
        return four
    elif value == 5:
        return five
    elif value == 6:
        return six
    elif value == 7:
        return seven
    elif value == 8:
        return eight
    elif value == 9:
        return nine
    elif value == 40:  # خانه خالی
        return (40, 40, 40)
    else:
        return WHITE


def draw_lattice():
    """رسم lattice (از منطق کد شما با تغییرات)"""
    for row in range(MAX_ROWS):
        for column in range(MAX_COLS):
            value = lattice[row][column]
            color = get_color(value)

            # فقط سطرهای تا current_row را رسم کن
            if row <= current_row:
                pygame.draw.rect(screen, color,
                                 [chessboard_x + (MARGIN + CELL_SIZE) * column + MARGIN,
                                  chessboard_y + (MARGIN + CELL_SIZE) * row + MARGIN,
                                  CELL_SIZE,
                                  CELL_SIZE])

                # نمایش عدد اگر خانه پر شده باشد
                if show_numbers and value != 40 and 0 <= value <= 9:
                    digit_text = digit_font.render(str(value), True, (0, 0, 0))
                    digit_rect = digit_text.get_rect(
                        center=(chessboard_x + (MARGIN + CELL_SIZE) * column + MARGIN + CELL_SIZE // 2,
                                chessboard_y + (MARGIN + CELL_SIZE) * row + MARGIN + CELL_SIZE // 2))
                    screen.blit(digit_text, digit_rect)

            # رسم خطوط شطرنجی برای خانه خالی
            elif row > current_row:
                pygame.draw.rect(screen, (60, 60, 60),
                                 [chessboard_x + (MARGIN + CELL_SIZE) * column + MARGIN,
                                  chessboard_y + (MARGIN + CELL_SIZE) * row + MARGIN,
                                  CELL_SIZE,
                                  CELL_SIZE], 1)


def draw_coordinates():
    """رسم شماره‌گذاری سطرها و ستون‌ها - بهبود یافته"""
    # شماره‌گذاری سطرها (سمت چپ) - رنگ روشن‌تر و فونت مناسب
    for row in range(0, total_rows, 2):
        y = chessboard_y + row * (CELL_SIZE + MARGIN) + (CELL_SIZE + MARGIN) // 2
        row_text = coord_font.render(str(row), True, (220, 220, 220))  # رنگ روشن‌تر
        text_x = chessboard_x - 35  # نزدیک‌تر
        if text_x >= 5:
            screen.blit(row_text, (text_x, y - row_text.get_height() // 2))

    # شماره‌گذاری سطرها (سمت راست)
    for row in range(0, total_rows, 2):
        y = chessboard_y + row * (CELL_SIZE + MARGIN) + (CELL_SIZE + MARGIN) // 2
        row_text = coord_font.render(str(row), True, (220, 220, 220))  # رنگ روشن‌تر
        text_x = chessboard_x + CHESSBOARD_WIDTH + 10  # نزدیک‌تر
        if text_x + row_text.get_width() <= WIDTH - 5:
            screen.blit(row_text, (text_x, y - row_text.get_height() // 2))

    # شماره‌گذاری ستون‌ها (بالا) - همه ستون‌ها را نمایش بده
    for col in range(0, MAX_COLS, 2):  # همه ستون‌ها یکی در میان
        x = chessboard_x + col * (CELL_SIZE + MARGIN) + (CELL_SIZE + MARGIN) // 2
        col_text = coord_font.render(str(col), True, (220, 220, 220))  # رنگ روشن‌تر
        text_y = chessboard_y - 20  # بالاتر
        if text_y >= 5:
            screen.blit(col_text, (x - col_text.get_width() // 2, text_y))


# ============ Main Game Loop ============
clock = pygame.time.Clock()
running = True

print("\n" + "=" * 60)
print("CONTROLS:")
print("SPACE: Toggle auto-step")
print("RIGHT: Next row")
print("LEFT: Previous row")
print("UP/DOWN: Change speed")
print("N: Toggle numbers visibility")
print("R: Reset to first row")
print("ESC: Exit")
print("=" * 60)

while running:
    current_time = time.time()

    # ============ Event Handling ============
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                auto_proceed = not auto_proceed
                print(f"Auto-step: {'ON' if auto_proceed else 'OFF'}")
            elif event.key == pygame.K_RIGHT:
                if current_row < total_rows - 1:
                    current_row += 1
                    print(f"Row: {current_row + 1}/{total_rows}")
            elif event.key == pygame.K_LEFT:
                if current_row > 0:
                    current_row -= 1
                    print(f"Row: {current_row + 1}/{total_rows}")
            elif event.key == pygame.K_UP:
                step_delay = max(0.3, step_delay - 0.1)
                print(f"Step delay: {step_delay:.1f}s")
            elif event.key == pygame.K_DOWN:
                step_delay = min(3.0, step_delay + 0.1)
                print(f"Step delay: {step_delay:.1f}s")
            elif event.key == pygame.K_n:
                show_numbers = not show_numbers
                print(f"Show numbers: {'ON' if show_numbers else 'OFF'}")
            elif event.key == pygame.K_r:
                current_row = 0
                print("Reset to first row")

    # ============ Auto Proceed Logic ============
    if auto_proceed and current_time - last_step_time > step_delay:
        if current_row < total_rows - 1:
            current_row += 1
            last_step_time = current_time
        else:
            auto_proceed = False

    # ============ Drawing ============
    screen.fill(BLACK)  # پس‌زمینه سیاه (همانند کد شما)

    # عنوان اصلی - دو خطی برای عدم خروج از صفحه
    title_line1 = title_font.render("MZ-method-Division by Two Cellular Automata(D2CA)", True, (100, 200, 255))

    title1_x = WIDTH // 2 - title_line1.get_width() // 2

    screen.blit(title_line1, (title1_x, 70))

    # اطلاعات اولیه
    middle_digit = num1[len(num1) // 2] if len(num1) % 2 == 1 else num1[len(num1) // 2 - 1]
    info_text = info_font.render(f"Initial Number: {n}  |  Center Digit: {middle_digit} at column {center_col}",
                                 True, (200, 200, 100))
    info_x = WIDTH // 2 - info_text.get_width() // 2
    screen.blit(info_text, (info_x, 130))

    # وضعیت فعلی
    status_text = status_font.render(
        f"Row: {current_row + 1}/{total_rows}  |  Auto-step: {'ON' if auto_proceed else 'OFF'}  |  Delay: {step_delay:.1f}s",
        True, (100, 255, 100)
    )
    status_x = WIDTH // 2 - status_text.get_width() // 2
    screen.blit(status_text, (status_x, 170))

    # ============ Drawing Chessboard ============
    # پس‌زمینه صفحه شطرنج
    pygame.draw.rect(screen, (30, 35, 45),
                     (chessboard_x - 10, chessboard_y - 10,
                      CHESSBOARD_WIDTH + 20, CHESSBOARD_HEIGHT + 20),
                     border_radius=8)

    # رسم lattice
    draw_lattice()

    # شماره‌گذاری
    draw_coordinates()

    # هایلایت سطر فعلی
    if current_row < total_rows:
        highlight_y = chessboard_y + current_row * (CELL_SIZE + MARGIN)
        pygame.draw.rect(screen, (255, 255, 100, 50),
                         (chessboard_x, highlight_y, CHESSBOARD_WIDTH, CELL_SIZE + MARGIN))
        pygame.draw.rect(screen, (255, 255, 100),
                         (chessboard_x, highlight_y, CHESSBOARD_WIDTH, CELL_SIZE + MARGIN), 2)

    # ============ Information Panel ============


    # ============ Control Panel ============
    control_panel_y = HEIGHT - 200  # 50 پیکسل بالاتر (تغییر)
    control_panel = pygame.Rect(WIDTH - 430, control_panel_y, 400, 170)
    pygame.draw.rect(screen, (25, 35, 45), control_panel, border_radius=8)
    pygame.draw.rect(screen, (70, 90, 110), control_panel, 2, border_radius=8)

    control_lines = [
        "CONTROLS:",
        "SPACE: Auto-step",
        "→ ← : Next/Prev row",
        "R: Reset   ESC: Exit"
    ]

    for i, line in enumerate(control_lines):
        color = (100, 200, 255) if i == 0 else (200, 220, 255)
        text = small_font.render(line, True, color)
        screen.blit(text, (WIDTH - 410, control_panel_y + 20 + i * 28))

    # ============ Progress Bar ============
    progress_y = chessboard_y + CHESSBOARD_HEIGHT + 20  # نزدیک‌تر به صفحه شطرنج
    progress_width = min(1000, CHESSBOARD_WIDTH)  # عرض محدود
    progress_x = chessboard_x + (CHESSBOARD_WIDTH - progress_width) // 2-160

    # اطمینان از اینکه Progress Bar در صفحه باشد
    if progress_y + 50 < HEIGHT:  # اگر فضای کافی وجود دارد
        pygame.draw.rect(screen, (40, 50, 60),
                         (progress_x, progress_y, progress_width, 20), border_radius=10)

        progress = (current_row + 1) / total_rows
        pygame.draw.rect(screen, (0, 180, 80),
                         (progress_x, progress_y, int(progress_width * progress), 20), border_radius=10)

        progress_text = info_font.render(f"Progress: {progress * 100:.1f}%  ({current_row + 1}/{total_rows} rows)",
                                         True, (200, 200, 100))
        progress_text_x = progress_x + progress_width // 2 - progress_text.get_width() // 2
        screen.blit(progress_text, (progress_text_x, progress_y + 25))

        # ============ Color Legend ============
        legend_y = progress_y + 60
        # اطمینان از اینکه Color Legend در صفحه باشد
        if legend_y + 50 < HEIGHT:
            legend_colors = [zero, one, two, three, four, five, six, seven, eight, nine]

            legend_title = small_font.render("Digits 0-9:", True, (200, 200, 200))
            screen.blit(legend_title, (progress_x, legend_y - 25))

            for i in range(10):
                color_rect = pygame.Rect(progress_x + i * 35, legend_y, 32, 32)
                pygame.draw.rect(screen, legend_colors[i], color_rect)
                pygame.draw.rect(screen, (255, 255, 255), color_rect, 1)

                num_label = coord_font.render(str(i), True, (0, 0, 0))
                label_rect = num_label.get_rect(center=color_rect.center)
                screen.blit(num_label, label_rect)

    pygame.display.flip()
    clock.tick(60)

# ============ Cleanup ============
pygame.quit()
print("\n" + "=" * 60)
print("ANIMATION COMPLETED")
print("=" * 60)
print(f"Final row reached: {current_row + 1}")
print("Pattern displayed according to original MZ-method logic!")
