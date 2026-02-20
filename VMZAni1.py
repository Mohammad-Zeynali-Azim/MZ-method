import pygame
import numpy as np
import time
import math
import os

# ============ تنظیمات Pygame ============
WIDTH, HEIGHT = 1550, 1000
BACKGROUND = (15, 20, 30)
TEXT_COLOR = (255, 255, 255)
DIGIT_COLOR = (100, 200, 255)
RESULT_COLOR = (100, 255, 100)
PROCESS_COLOR = (255, 200, 100)
PARALLEL_COLOR = (255, 100, 255)
SEQUENTIAL_COLOR = (255, 150, 50)
QUOTIENT_COLOR = (100, 255, 255)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)
BUTTON_CLICK_COLOR = (50, 110, 160)

# ============ مسیر تصویر ============
# مسیر تصویر خود را اینجا قرار دهید
IMAGE_PATH = "FPGA.jpg"  # تصویر با ابعاد 600x500

# ============ متغیرهای حالت ============
fpga_window_open = False
quotient_window_open = False
button_hovered = False
button_clicked = False

s = input("Enter a number (for analysis): ")

# ============ الگوریتم تقسیم بر دو با آنالیز موازی ============
def parallel_analysis_division(s):
    """ آنالیز موازی بودن عملیات در الگوریتم تقسیم بر دو """
    arr = np.frombuffer(s.encode(), dtype=np.uint8) - 48
    n = len(arr)

    # گروه‌بندی عملیات موازی
    parallel_groups = []

    # گروه 1: محاسبه پارتی (زوج/فرد) - کاملاً موازی
    parity_group = {
        'name': 'Parity Calculation',
        'operations': [],
        'parallel': True,
        'description': 'محاسبه زوج/فرد بودن تمام ارقام به صورت موازی',
        'start_index': 0,
        'end_index': n - 1,
        'original_digits': arr.tolist()
    }

    for i in range(n - 1):
        parity_group['operations'].append({
            'index': i,
            'operation': f'digit[{i}] & 1',
            'input': arr[i],
            'output': arr[i] & 1
        })

    # گروه 2: محاسبه first_digit - تکی (غیرموازی)
    first_digit_group = {
        'name': 'First Digit Division',
        'operations': [{
            'index': 0,
            'operation': 'digit[0] >> 1',
            'input': arr[0],
            'output': arr[0] >> 1
        }],
        'parallel': False,
        'description': 'تقسیم رقم اول (عملیات تکی)',
        'start_index': 0,
        'end_index': 0,
        'original_digits': arr.tolist()
    }

    # گروه 3: ضرب پارتی در 5 - موازی
    multiply_group = {
        'name': 'Multiply by 5',
        'operations': [],
        'parallel': True,
        'description': 'ضرب ارقام فرد در ۵ به صورت موازی',
        'start_index': 0,
        'end_index': n - 2,
        'original_digits': arr.tolist()
    }

    parity_vals = arr[:-1] & 1
    for i in range(n - 1):
        if parity_vals[i] == 1:
            multiply_group['operations'].append({
                'index': i,
                'operation': f'1 × 5',
                'input': 1,
                'output': 5
            })
        else:
            multiply_group['operations'].append({
                'index': i,
                'operation': f'0 × 5',
                'input': 0,
                'output': 0
            })

    # گروه 4: Shift راست ارقام بعدی - موازی
    shift_group = {
        'name': 'Right Shift',
        'operations': [],
        'parallel': True,
        'description': 'تقسیم ارقام بعدی بر ۲ به صورت موازی',
        'start_index': 1,
        'end_index': n - 1,
        'original_digits': arr.tolist()
    }

    for i in range(1, n):
        shift_group['operations'].append({
            'index': i,
            'operation': f'digit[{i}] >> 1',
            'input': arr[i],
            'output': arr[i] >> 1
        })

    # گروه 5: جمع نتایج - نیمه موازی (وابستگی داده‌ای)
    addition_group = {
        'name': 'Addition',
        'operations': [],
        'parallel': False,  # وابستگی داده‌ای دارد
        'description': 'جمع نتایج (وابستگی داده‌ای - نیمه موازی)',
        'start_index': 0,
        'end_index': n - 1,
        'original_digits': arr.tolist(),
        'is_addition': True  # علامت مخصوص گروه جمع
    }

    # محاسبه نتایج برای نمایش
    first_digit = arr[0] >> 1
    parity_multiplied = (arr[:-1] & 1) * 5
    shifted_digits = arr[1:] >> 1

    if first_digit > 0:
        result = np.concatenate(([first_digit], (parity_multiplied + shifted_digits).tolist()))
    else:
        result = (parity_multiplied + shifted_digits).tolist()

    # گروه 6: نمایش نتیجه نهایی (Quotient)
    quotient_group = {
        'name': 'Quotient',
        'operations': [],
        'parallel': True,  # نمایش موازی
        'description': 'نتیجه نهایی تقسیم (خارج قسمت)',
        'start_index': 0,
        'end_index': len(result) - 1,
        'original_digits': arr.tolist(),
        'is_quotient': True
    }

    # اضافه کردن عملیات جمع (با فاصله بیشتر و کوچکتر)
    for i in range(len(result)):
        if i == 0:
            addition_group['operations'].append({
                'index': i,
                'operation': f'first_digit',
                'input': first_digit,
                'output': result[i]
            })
        elif i == len(result) - 1:
            addition_group['operations'].append({
                'index': i,
                'operation': f'5×parity[{i - 1}] + shift[{i}]',
                'input': f'{parity_multiplied[i - 1]}+{shifted_digits[i - 1]}',
                'output': result[i]
            })
        else:
            addition_group['operations'].append({
                'index': i,
                'operation': f'5×parity[{i - 1}] + shift[{i}]',
                'input': f'{parity_multiplied[i - 1]}+{shifted_digits[i - 1]}',
                'output': result[i]
            })

    # عملیات Quotient (همان نتیجه اما با فرمت متفاوت)
    for i, val in enumerate(result):
        quotient_group['operations'].append({
            'index': i,
            'operation': f'Q[{i}]',
            'input': '',
            'output': val,
            'is_final': True
        })

    # جمع‌آوری تمام گروه‌ها
    all_groups = [
        first_digit_group,  # باید اول باشد (وابستگی)
        parity_group,
        multiply_group,
        shift_group,
        addition_group,  # گروه جمع با فاصله بیشتر
        quotient_group  # گروه نتیجه نهایی
    ]

    return all_groups, result, arr


# ============ Pygame Setup ============
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DN2: Parallel Operations Analysis with Quotient (Manual Control)")
clock = pygame.time.Clock()

# فونت‌ها
title_font = pygame.font.SysFont('Arial', 42, bold=True)
group_font = pygame.font.SysFont('Arial', 32, bold=True)
info_font = pygame.font.SysFont('Arial', 28)
op_font = pygame.font.SysFont('Arial', 20)  # کوچکتر شده
small_font = pygame.font.SysFont('Arial', 18)  # کوچکتر شده
digit_display_font = pygame.font.SysFont('Arial', 26, bold=True)
button_font = pygame.font.SysFont('Arial', 30, bold=True)

# ============ دریافت ورودی ============
print("=" * 60)
print("MZ-METHOD: PARALLEL OPERATIONS ANALYSIS WITH QUOTIENT")
print("=" * 60)
#s = input("Enter a number (for analysis): ")
print(f"\nAnalyzing number: {s} ({len(s)} digits)")
print("Analyzing parallel operations...")

# ============ اجرای آنالیز ============
parallel_groups, result, original_digits = parallel_analysis_division(s)
result_str = ''.join(map(str, result))
print(f"\nAnalysis complete!")
print(f"Number of operation groups: {len(parallel_groups)}")
print(f"Result (Quotient): {result_str}")

# ============ متغیرهای انیمیشن ============
current_group = 0
current_op = 0
running = True

print("\nControls:")
print("RIGHT/LEFT: Next/Previous operation")
print("UP/DOWN: Next/Previous group")
print("R: Reset to first operation")
print("ESC: Exit")
print("\nUse arrow keys to navigate through operations manually...")


# ============ تابع نمایش ارقام اصلی بالای مستطیل‌ها ============
def draw_original_digits(screen, digits, x, y, width, highlight_index=None):
    """ نمایش ارقام اصلی در بالای گروه عملیات """
    n = len(digits)
    digit_spacing = min(50, width // (n + 1))
    start_x = x + (width - (n * digit_spacing)) // 2

    # عنوان
    original_title = info_font.render("Original Digits:", True, DIGIT_COLOR)
    screen.blit(original_title, (start_x, y - 40))

    # نمایش ارقام
    for i, digit in enumerate(digits):
        digit_x = start_x + i * digit_spacing
        digit_y = y + 20

        # رنگ برای هایلایت
        if highlight_index == i:
            bg_color = (60, 80, 100)
            border_color = (255, 255, 100)
        else:
            bg_color = (40, 60, 80)
            border_color = DIGIT_COLOR

        # مستطیل رقم
        pygame.draw.rect(screen, bg_color, (digit_x - 18, digit_y - 18, 36, 36), border_radius=6)
        pygame.draw.rect(screen, border_color, (digit_x - 18, digit_y - 18, 36, 36), 2, border_radius=6)

        # نمایش رقم
        digit_text = digit_display_font.render(str(digit), True, (255, 255, 200))
        digit_rect = digit_text.get_rect(center=(digit_x, digit_y))
        screen.blit(digit_text, digit_rect)

        # نمایش ایندکس
        idx_text = small_font.render(str(i), True, (150, 150, 150))
        idx_rect = idx_text.get_rect(center=(digit_x, digit_y + 25))
        screen.blit(idx_text, idx_rect)


# ============ تابع رسم گروه عملیات ============
def draw_operation_group(screen, group, group_index, x, y, width, height, is_active=False, active_op=None):
    """ رسم یک گروه عملیات موازی """
    # نمایش ارقام اصلی در بالای گروه
    if 'original_digits' in group:
        draw_original_digits(screen, group['original_digits'], x, y + 20, width)
        y += 80  # فاصله از ارقام اصلی

    # رنگ پس‌زمینه گروه
    if group.get('is_quotient', False):  # گروه Quotient رنگ مخصوص
        if is_active:
            bg_color = (30, 60, 70)
            border_color = QUOTIENT_COLOR
        else:
            bg_color = (25, 50, 60)
            border_color = (80, 160, 180)
    elif is_active:
        bg_color = (40, 50, 70) if group['parallel'] else (60, 40, 40)
        border_color = (100, 200, 255) if group['parallel'] else (255, 100, 100)
    else:
        bg_color = (30, 40, 55) if group['parallel'] else (45, 35, 35)
        border_color = (70, 90, 110)

    # مستطیل گروه
    group_rect = pygame.Rect(x, y, width, height - 80)  # کم کردن ارتفاع برای ارقام اصلی
    pygame.draw.rect(screen, bg_color, group_rect, border_radius=10)
    pygame.draw.rect(screen, border_color, group_rect, 3, border_radius=10)

    # عنوان گروه
    if group.get('is_quotient', False):
        group_name = group_font.render("QUOTIENT", True, QUOTIENT_COLOR)
    else:
        group_name = group_font.render(group['name'], True, PARALLEL_COLOR if group['parallel'] else SEQUENTIAL_COLOR)
    screen.blit(group_name, (x + 20, y + 15))

    # وضعیت موازی/غیرموازی (برای گروه‌های غیر Quotient)
    if not group.get('is_quotient', False):
        parallel_status = "PARALLEL" if group['parallel'] else "SEQUENTIAL"
        status_color = PARALLEL_COLOR if group['parallel'] else SEQUENTIAL_COLOR
        status_text = info_font.render(parallel_status, True, status_color)
        screen.blit(status_text, (x + width - 150, y + 20))

    # توضیحات
    desc_text = op_font.render(group['description'], True, (200, 200, 200))
    screen.blit(desc_text, (x + 20, y + 55))

    # نمایش عملیات‌ها
    ops_y = y + 90

    # تنظیمات ویژه برای گروه جمع
    if group.get('is_addition', False):
        max_ops_per_row = min(8, len(group['operations']))  # تعداد کمتر در هر ردیف
        op_width = 175  # عرض کمتر
        op_height = 70  # ارتفاع کمتر
        h_spacing = 30  # فاصله افقی بیشتر
        v_spacing = 25  # فاصله عمودی بیشتر
        font_size = op_font
    else:
        max_ops_per_row = min(10, len(group['operations']))
        op_width = 140
        op_height = 65
        h_spacing = 10
        v_spacing = 10
        font_size = op_font

    for i, op in enumerate(group['operations']):
        if i >= 20:  # محدودیت نمایش
            more_text = op_font.render(f"... +{len(group['operations']) - 20} more", True, (150, 150, 150))
            screen.blit(more_text, (x + 20, ops_y + 40))
            break

        row = i // max_ops_per_row
        col = i % max_ops_per_row

        # فاصله بیشتر برای گروه جمع
        if group.get('is_addition', False):
            op_x = x + 30 + col * (op_width + h_spacing)
            op_y = ops_y + row * (op_height + v_spacing)
        else:
            op_x = x + 30 + col * (op_width + h_spacing)
            op_y = ops_y + row * (op_height + v_spacing)

        # رنگ عملیات فعال
        if is_active and active_op == i:
            if group.get('is_quotient', False):
                op_bg_color = (40, 80, 90)
                op_border_color = QUOTIENT_COLOR
            elif group['parallel']:
                op_bg_color = (60, 70, 90)
                op_border_color = (255, 255, 100)
            else:
                op_bg_color = (80, 50, 50)
                op_border_color = (255, 200, 100)
        else:
            if group.get('is_quotient', False):
                op_bg_color = (35, 65, 75)
                op_border_color = (90, 180, 200)
            elif group['parallel']:
                op_bg_color = (40, 50, 65)
                op_border_color = (90, 110, 130)
            else:
                op_bg_color = (55, 40, 40)
                op_border_color = (130, 90, 90)

        # مستطیل عملیات (کوچکتر برای گروه جمع)
        if group.get('is_addition', False):
            op_rect = pygame.Rect(op_x, op_y, op_width, op_height)
        else:
            op_rect = pygame.Rect(op_x, op_y, op_width, op_height)

        pygame.draw.rect(screen, op_bg_color, op_rect, border_radius=6)
        pygame.draw.rect(screen, op_border_color, op_rect, 2, border_radius=6)

        # نمایش عملیات
        if 'index' in op:
            if group.get('is_quotient', False):
                idx_text = small_font.render(f"Q[{op['index']}]", True, (150, 250, 255))
            else:
                idx_text = small_font.render(f"Idx: {op['index']}", True, (150, 200, 255))
            screen.blit(idx_text, (op_x + 10, op_y + 8))

        if group.get('is_quotient', False):
            # برای Quotient فقط نتیجه را نمایش بده
            op_text = font_size.render(f"Result", True, (255, 255, 200))
            screen.blit(op_text, (op_x + 10, op_y + 25))
        else:
            op_text = font_size.render(op['operation'], True, (255, 255, 200))
            screen.blit(op_text, (op_x + 10, op_y + 25))

        # نمایش خروجی
        if 'output' in op:
            if group.get('is_quotient', False):
                # برای Quotient، خروجی را بزرگ‌تر نمایش بده
                output_text = digit_display_font.render(str(op['output']), True, QUOTIENT_COLOR)
                output_rect = output_text.get_rect(center=(op_x + op_width // 2, op_y + 40))
                screen.blit(output_text, output_rect)
            else:
                output_text = small_font.render(f"→ {op['output']}", True, RESULT_COLOR)
                if group.get('is_addition', False):
                    screen.blit(output_text, (op_x + 85, op_y + 35))  # موقعیت متفاوت برای جمع
                else:
                    screen.blit(output_text, (op_x + 100, op_y + 35))

    return height


# ============ تابع رسم دکمه ============
def draw_fpga_button(screen, mouse_pos, show_button=True):
    """ رسم دکمه FPGA Circuit """
    global button_hovered, button_clicked

    # اگر نباید دکمه نمایش داده شود یا در پنجره‌های دیگر هستیم
    if not show_button or quotient_window_open or fpga_window_open:
        return None

    # محاسبه موقعیت وسط بین کنترل و info
    button_width, button_height = 200, 60
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT - 220  # موقعیت مناسب بین کنترل و info

    # ایجاد مستطیل دکمه
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # تشخیص hover
    button_hovered = button_rect.collidepoint(mouse_pos)

    # انتخاب رنگ
    if button_clicked:
        color = BUTTON_CLICK_COLOR
    elif button_hovered:
        color = BUTTON_HOVER_COLOR
    else:
        color = BUTTON_COLOR

    # رسم دکمه با سایه
    pygame.draw.rect(screen, (color[0] // 2, color[1] // 2, color[2] // 2),
                     (button_x + 5, button_y + 5, button_width, button_height),
                     border_radius=12)
    pygame.draw.rect(screen, color, button_rect, border_radius=10)
    pygame.draw.rect(screen, (200, 200, 255), button_rect, 3, border_radius=10)

    # نوشته دکمه
    text = button_font.render("FPGA Circuit", True, (255, 255, 255))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    return button_rect


# ============ تابع نمایش صفحه FPGA ============
def draw_fpga_window(screen):
    """ نمایش صفحه FPGA در وسط صفحه اصلی """
    global fpga_window_open

    # اندازه پنجره
    window_width, window_height = 800, 600
    window_x = WIDTH // 2 - window_width // 2
    window_y = HEIGHT // 2 - window_height // 2

    # پس‌زمینه شفاف
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # پنجره اصلی
    window_rect = pygame.Rect(window_x, window_y, window_width, window_height)
    pygame.draw.rect(screen, (20, 30, 40), window_rect, border_radius=15)
    pygame.draw.rect(screen, (70, 130, 180), window_rect, 4, border_radius=15)

    # عنوان
    title = title_font.render("FPGA Circuit of MZ-method/DN2 ", True, (100, 200, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, window_y + 30))

    # خط جداکننده
    pygame.draw.line(screen, (70, 130, 180),
                     (window_x + 50, window_y + 100),
                     (window_x + window_width - 50, window_y + 100), 3)

    # ============ بخش تصویر ============
    # بارگذاری و نمایش تصویر 600x500
    try:
        if os.path.exists(IMAGE_PATH):
            # بارگذاری تصویر
            circuit_image = pygame.image.load(IMAGE_PATH)
            # تغییر اندازه تصویر به 600x500
            circuit_image = pygame.transform.scale(circuit_image, (780, 450))

            # موقعیت نمایش تصویر (مرکز پنجره)
            image_x = window_x + (window_width - 780) // 2
            image_y = window_y + 120

            # نمایش تصویر
            screen.blit(circuit_image, (image_x, image_y))

            # عنوان تصویر
            image_title = info_font.render("", True, (150, 200, 255))
            screen.blit(image_title, (window_x + (window_width - image_title.get_width()) // 2, window_y + 80))
        else:
            # اگر تصویر پیدا نشد، پیام خطا نمایش دهید
            error_text = info_font.render(f"Image not found: {IMAGE_PATH}", True, (255, 100, 100))
            screen.blit(error_text, (window_x + 100, window_y + 150))

            # جایگزین: یک مستطیل خاکستری با ابعاد 600x500
            placeholder_rect = pygame.Rect(window_x + 100, window_y + 200, 600, 500)
            pygame.draw.rect(screen, (50, 50, 50), placeholder_rect)
            pygame.draw.rect(screen, (100, 100, 100), placeholder_rect, 2)

            placeholder_text = info_font.render("600 x 500 Image Placeholder", True, (150, 150, 150))
            screen.blit(placeholder_text, (window_x + 250, window_y + 450))
    except Exception as e:
        error_text = info_font.render(f"Error loading image: {str(e)[:30]}", True, (255, 100, 100))
        screen.blit(error_text, (window_x + 100, window_y + 150))

    # ============ دکمه بازگشت ============
    return_button_y = window_y + window_height - 80
   # return_button = pygame.Rect(WIDTH // 2 - 100, return_button_y, 200, 60)
   # pygame.draw.rect(screen, (40, 70, 100), return_button, border_radius=10)
   # pygame.draw.rect(screen, (100, 200, 255), return_button, 3, border_radius=10)

    #return_text = button_font.render("Back (R)", True, (255, 255, 255))
    #return_rect = return_text.get_rect(center=return_button.center)
    #screen.blit(return_text, return_rect)

    # متن راهنما
    help_text = info_font.render("Press 'R' to return to main screen", True, (255, 200, 100))
    screen.blit(help_text, (WIDTH // 2 - help_text.get_width() // 2, return_button_y +100))


# ============ تابع نمایش صفحه Quotient ============
def draw_quotient_window(screen):
    """ نمایش صفحه Quotient در کل صفحه """
    global quotient_window_open

    # پس‌زمینه صفحه Quotient
    screen.fill((10, 15, 25))  # رنگ پس‌زمینه تیره‌تر

    # عنوان اصلی
    title = title_font.render("QUOTIENT RESULT DISPLAY", True, QUOTIENT_COLOR)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    # خط جداکننده
    pygame.draw.line(screen, QUOTIENT_COLOR, (100, 120), (WIDTH - 100, 120), 3)

    # نمایش نتیجه Quotient بزرگ در وسط
    quotient_display = pygame.font.SysFont('Arial', 80, bold=True).render(result_str, True, QUOTIENT_COLOR)
    screen.blit(quotient_display, (WIDTH // 2 - quotient_display.get_width() // 2, HEIGHT // 2 - 100))

    # زیرنویس
    subtitle = info_font.render("Final Quotient Result", True, (200, 200, 200))
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2))

    # نمایش ارقام Quotient به صورت جداگانه
    digit_y = HEIGHT // 2 + 80
    digit_spacing = 60
    start_x = WIDTH // 2 - (len(result) * digit_spacing) // 2

    for i, digit in enumerate(result):
        digit_x = start_x + i * digit_spacing

        # کادر Quotient با سایه
        pygame.draw.rect(screen, (20, 40, 50), (digit_x - 25, digit_y - 25, 50, 50), border_radius=10)
        pygame.draw.rect(screen, QUOTIENT_COLOR, (digit_x - 25, digit_y - 25, 50, 50), 3, border_radius=10)

        # رقم
        digit_text = pygame.font.SysFont('Arial', 36, bold=True).render(str(digit), True, (255, 255, 200))
        digit_rect = digit_text.get_rect(center=(digit_x, digit_y))
        screen.blit(digit_text, digit_rect)

        # ایندکس
        idx_text = small_font.render(f"Q[{i}]", True, (150, 200, 200))
        idx_rect = idx_text.get_rect(center=(digit_x, digit_y + 35))
        screen.blit(idx_text, idx_rect)

    # اطلاعات اضافی
    info_y = digit_y + 100

    info_lines = [
        f"Input Number: {s}",
        f"Quotient Length: {len(result)} digits",
        f"Original Digits: {len(s)}",
        f"Parallel Operations: {sum(len(g['operations']) for g in parallel_groups if g['parallel'])}"
    ]

    for i, line in enumerate(info_lines):
        text = info_font.render(line, True, (200, 220, 240))
        screen.blit(text, (WIDTH // 2 - 300, info_y + i * 40))

    # دکمه بازگشت
    return_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 60)
    pygame.draw.rect(screen, (40, 70, 100), return_button, border_radius=10)
    pygame.draw.rect(screen, QUOTIENT_COLOR, return_button, 3, border_radius=10)

    return_text = button_font.render("Back (R)", True, (255, 255, 255))
    return_rect = return_text.get_rect(center=return_button.center)
    screen.blit(return_text, return_rect)

    # متن راهنما
    help_text = info_font.render("Press 'R' to return to main screen", True, (255, 200, 100))
    screen.blit(help_text, (WIDTH // 2 - help_text.get_width() // 2, HEIGHT - 180))


# ============ تابع رسم صفحه اصلی ============
def draw_main_screen(screen, mouse_pos):
    """ رسم صفحه اصلی """
    # عنوان اصلی
    title = title_font.render("MZ-method: Parallel Operations Analysis with Quotient Display (MANUAL CONTROL)", True,
                              (0, 255, 100))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    # نمایش عدد اصلی و نتیجه (فقط در صفحه اصلی)
    if not quotient_window_open:
        input_display = info_font.render(f"MZ-METHOD: PARALLEL OPERATIONS ANALYSIS WITH QUOTIENT ", True, (200, 200, 100))
        screen.blit(input_display, (WIDTH // 2 - input_display.get_width() // 2, 70))

    # ============ نمایش گروه‌های عملیات ============
    group_width = 1550
    group_height = 400  # ارتفاع بیشتر برای گروه جمع
    group_x = 25
    group_y = 120

    # فقط گروه فعلی را نمایش بده
    if current_group < len(parallel_groups):
        group = parallel_groups[current_group]
        draw_operation_group(screen, group, current_group, group_x, group_y, group_width, group_height, True,
                             current_op)

    # ============ نمایش خلاصه نتایج ============
    summary_y = group_y + group_height + 30

    # بررسی آیا گروه فعلی Quotient است
    current_group_is_quotient = parallel_groups[current_group].get('is_quotient', False) if current_group < len(
        parallel_groups) else False

    if current_group == len(parallel_groups) - 1 and current_group_is_quotient:
        # اگر در گروه Quotient هستیم، نمایش ویژه
        summary_title = info_font.render("FINAL QUOTIENT RESULT", True, QUOTIENT_COLOR)
        screen.blit(summary_title, (WIDTH // 2 - summary_title.get_width() // 2, summary_y))

        # نمایش Quotient در یک خط
       #quotient_str_display = f"Quotient: {result_str}"
        #quotient_display = group_font.render(quotient_str_display, True, QUOTIENT_COLOR)
        #screen.blit(quotient_display, (WIDTH // 2 - quotient_display.get_width() // 2, summary_y + 40))

        # نمایش هر رقم Quotient جداگانه
        digit_spacing = 50
        start_x = WIDTH // 2 - (len(result) * digit_spacing) // 2

        for i, digit in enumerate(result):
            digit_x = start_x + i * digit_spacing
            digit_y = summary_y + 100

            # کادر Quotient
            pygame.draw.rect(screen, (30, 70, 80), (digit_x - 20, digit_y - 20, 40, 40), border_radius=8)
            pygame.draw.rect(screen, QUOTIENT_COLOR, (digit_x - 20, digit_y - 20, 40, 40), 2, border_radius=8)

            # رقم
            digit_text = digit_display_font.render(str(digit), True, (255, 255, 200))
            digit_rect = digit_text.get_rect(center=(digit_x, digit_y))
            screen.blit(digit_text, digit_rect)

            # ایندکس
            idx_text = small_font.render(f"Q[{i}]", True, (150, 200, 200))
            idx_rect = idx_text.get_rect(center=(digit_x, digit_y + 30))
            screen.blit(idx_text, idx_rect)

        summary_y += 180

    # ============ نمایش نمودار موازی بودن ============
    timeline_y = summary_y + 20
    timeline_height = 150

    # عنوان Timeline
    timeline_title = info_font.render("Parallel Execution Timeline", True, (255, 255, 100))
    screen.blit(timeline_title, (WIDTH // 2 - timeline_title.get_width() // 2, timeline_y - 25))

    # محور زمان
    timeline_start_x = 100
    timeline_end_x = WIDTH - 100
    timeline_center_y = timeline_y + timeline_height // 2

    pygame.draw.line(screen, (100, 100, 100),
                     (timeline_start_x, timeline_center_y),
                     (timeline_end_x, timeline_center_y), 3)

    # نمایش گروه‌ها روی Timeline
    group_spacing = (timeline_end_x - timeline_start_x) / len(parallel_groups)

    for i, group in enumerate(parallel_groups):
        group_x_pos = timeline_start_x + i * group_spacing + group_spacing / 2

        # رنگ گروه
        if group.get('is_quotient', False):
            group_color = QUOTIENT_COLOR
        else:
            group_color = PARALLEL_COLOR if group['parallel'] else SEQUENTIAL_COLOR

        # دایره گروه
        pygame.draw.circle(screen, group_color, (int(group_x_pos), timeline_center_y), 18)
        pygame.draw.circle(screen, (255, 255, 255), (int(group_x_pos), timeline_center_y), 18, 2)

        # نام کوتاه گروه
        if group.get('is_quotient', False):
            group_name_short = "QUOT"
        else:
            group_name_short = group['name'].split()[0][:4]

        name_text = small_font.render(group_name_short, True, group_color)
        screen.blit(name_text, (int(group_x_pos) - 25, timeline_center_y - 35))

        # هایلایت گروه فعلی
        if i == current_group:
            pygame.draw.circle(screen, (255, 255, 100), (int(group_x_pos), timeline_center_y), 22, 3)

    # ============ پانل اطلاعات ============
    info_panel_y = timeline_y + timeline_height + 20
    info_panel = pygame.Rect(50, info_panel_y, 500, 180)
    pygame.draw.rect(screen, (25, 35, 45), info_panel, border_radius=10)
    pygame.draw.rect(screen, (70, 90, 110), info_panel, 2, border_radius=10)

    # محاسبه آمار
    total_ops = sum(len(g['operations']) for g in parallel_groups if not g.get('is_quotient', False))
    parallel_ops = sum(
        len(g['operations']) for g in parallel_groups if g['parallel'] and not g.get('is_quotient', False))
    parallel_percent = (parallel_ops / total_ops * 100) if total_ops > 0 else 0

    # اطلاعات گروه فعلی
    current_group_info = parallel_groups[current_group]
    current_group_name = current_group_info['name']
    current_group_ops = len(current_group_info['operations'])
    current_group_type = "PARALLEL" if current_group_info['parallel'] else "SEQUENTIAL"

    info_lines = [
        f"Input Digits: {len(s)}",
        f"Quotient Digits: {len(result)}",
        f"Current Group: {current_group_name}",
        f"Group Type: {current_group_type}",
        f"Ops in Group: {current_op + 1}/{current_group_ops}",
        f"Parallel Ops: {parallel_percent:.1f}%",
    ]

    for i, line in enumerate(info_lines):
        text = info_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (70, info_panel_y + 15 + i * 28))

    # ============ پانل راهنما ============
    help_panel = pygame.Rect(WIDTH - 550, info_panel_y, 500, 180)
    pygame.draw.rect(screen, (25, 35, 45), help_panel, border_radius=10)
    pygame.draw.rect(screen, (70, 90, 110), help_panel, 2, border_radius=10)

    help_lines = [
        "MANUAL CONTROL MODE",
        "→ : Next operation",
        "← : Previous operation",
        "↑ : Next group",
        "↓ : Previous group",
        "R : Reset to first",
        "Q : View Quotient",
        "ESC: Exit program"
    ]

    for i, line in enumerate(help_lines):
        color = (100, 255, 150) if i == 0 else (200, 200, 200)
        text = info_font.render(line, True, color)
        screen.blit(text, (WIDTH - 530, info_panel_y + 15 + i * 28))

    # ============ دکمه FPGA Circuit ============
    # تغییر مهم: اگر گروه فعلی Quotient است، دکمه FPGA را نمایش نده
    if not quotient_window_open and not current_group_is_quotient:
        fpga_button = draw_fpga_button(screen, mouse_pos, show_button=True)
    else:
        # دکمه FPGA را نمایش نده
        pass

    # ============ Progress Bar ============
    if len(parallel_groups) > 0:
        total_ops_all = sum(len(g['operations']) for g in parallel_groups)
        current_total_op = sum(len(parallel_groups[i]['operations']) for i in range(current_group)) + current_op + 1
        progress = current_total_op / total_ops_all

        bar_width = 600
        bar_height = 20
        bar_x = WIDTH // 2 - bar_width // 2
        bar_y = HEIGHT - 40

        pygame.draw.rect(screen, (40, 50, 60), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 180, 80), (bar_x, bar_y, int(bar_width * progress), bar_height))

        progress_text = f"Progress: {current_total_op}/{total_ops_all} operations ({progress * 100:.1f}%)"
        text = info_font.render(progress_text, True, (255, 255, 200))
        screen.blit(text, (bar_x + bar_width // 2 - text.get_width() // 2, bar_y - 30))


# ============ حلقه اصلی ============
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                if fpga_window_open:
                    fpga_window_open = False  # بستن پنجره FPGA
                elif quotient_window_open:
                    quotient_window_open = False  # بستن پنجره Quotient
                else:
                    current_group = 0
                    current_op = 0
                    print("Reset to first operation")
            elif event.key == pygame.K_q and not fpga_window_open:
                # کلید Q برای نمایش صفحه Quotient
                quotient_window_open = not quotient_window_open
                if quotient_window_open:
                    print("Quotient window opened")
                else:
                    print("Quotient window closed")
            elif not fpga_window_open and not quotient_window_open:
                # کنترل‌های اصلی فقط در صفحه اصلی فعال باشند
                if event.key == pygame.K_RIGHT:
                    if current_group < len(parallel_groups):
                        if current_op < len(parallel_groups[current_group]['operations']) - 1:
                            current_op += 1
                            print(f"Operation {current_op + 1}/{len(parallel_groups[current_group]['operations'])}")
                elif event.key == pygame.K_LEFT:
                    if current_op > 0:
                        current_op -= 1
                        print(f"Operation {current_op + 1}/{len(parallel_groups[current_group]['operations'])}")
                elif event.key == pygame.K_UP:
                    if current_group < len(parallel_groups) - 1:
                        current_group += 1
                        current_op = 0
                        print(
                            f"Group {current_group + 1}/{len(parallel_groups)}: {parallel_groups[current_group]['name']}")
                elif event.key == pygame.K_DOWN:
                    if current_group > 0:
                        current_group -= 1
                        current_op = 0
                        print(
                            f"Group {current_group + 1}/{len(parallel_groups)}: {parallel_groups[current_group]['name']}")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # کلیک چپ
                # بررسی کلیک روی دکمه FPGA (فقط در صفحه اصلی و اگر دکمه نمایش داده شود)
                if not fpga_window_open and not quotient_window_open:
                    # بررسی آیا گروه فعلی Quotient نیست
                    current_group_is_quotient = parallel_groups[current_group].get('is_quotient',
                                                                                   False) if current_group < len(
                        parallel_groups) else False
                    if not current_group_is_quotient:
                        temp_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 220, 200, 60)
                        if temp_button.collidepoint(mouse_pos):
                            button_clicked = True
                            fpga_window_open = True
                            print("FPGA Circuit window opened")

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                button_clicked = False

    # ============ رسم صفحه ============
    screen.fill(BACKGROUND)

    if fpga_window_open:
        # نمایش پنجره FPGA
        draw_fpga_window(screen)
    elif quotient_window_open:
        # نمایش پنجره Quotient
        draw_quotient_window(screen)
    else:
        # نمایش صفحه اصلی
        draw_main_screen(screen, mouse_pos)

    pygame.display.flip()
    clock.tick(60)

# ============ پایان ============
pygame.quit()
print("\n" + "=" * 60)
print("ANALYSIS COMPLETED WITH QUOTIENT DISPLAY")
print("=" * 60)

# چاپ نتایج
print(f"\nInput Number: {s}")
print(f"Final Quotient: {result_str}")
print(f"Quotient Length: {len(result)} digits")