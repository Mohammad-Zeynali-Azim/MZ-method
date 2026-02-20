import pygame
import sys
import os
import subprocess
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1600, 900
BACKGROUND_COLOR = (15, 25, 35)
TITLE_COLOR = (100, 200, 255)
SUBTITLE_COLOR = (200, 100, 255)
BUTTON_COLOR = (30, 60, 90)
BUTTON_HOVER_COLOR = (50, 100, 150)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_BORDER_COLOR = (80, 150, 200)
BOX_COLOR = (25, 40, 60)
BOX_BORDER_COLOR = (100, 150, 200)
BOX_TITLE_COLOR = (255, 200, 100)
HELP_BOX_COLOR = (40, 55, 75)
HELP_BOX_BORDER_COLOR = (150, 100, 200)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Division by Two Universe - Launcher")
clock = pygame.time.Clock()

# Fonts (reduced main title font size)
title_font = pygame.font.SysFont('Arial', 56, bold=True)  # Reduced from 64
subtitle_font = pygame.font.SysFont('Arial', 34, italic=True)  # Reduced from 36
button_font = pygame.font.SysFont('Arial', 28)
status_font = pygame.font.SysFont('Arial', 22)  # Reduced from 24
box_title_font = pygame.font.SysFont('Arial', 30, bold=True)  # Reduced from 32
box_text_font = pygame.font.SysFont('Arial', 24)  # Reduced from 26
help_font = pygame.font.SysFont('Arial', 22)


# Button class
class Button:
    def __init__(self, x, y, width, height, text, program_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.program_path = program_path
        self.hovered = False

    def draw(self, surface):
        # Draw button
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, BUTTON_BORDER_COLOR, self.rect, 3, border_radius=12)

        # Draw text
        text_surf = button_font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered

    def execute(self):
        """Execute the associated program"""
        try:
            if os.path.exists(self.program_path):
                # For Windows
                if sys.platform == "win32":
                    os.startfile(self.program_path)
                # For Mac/Linux
                else:
                    subprocess.Popen([self.program_path])
                return f"Executed: {os.path.basename(self.program_path)}"
            else:
                # Try with .py extension
                if os.path.exists(self.program_path + ".py"):
                    subprocess.Popen([sys.executable, self.program_path + ".py"])
                    return f"Executed: {os.path.basename(self.program_path)}.py"
                else:
                    # Try .exe extension
                    if os.path.exists(self.program_path + ".exe"):
                        subprocess.Popen([self.program_path + ".exe"])
                        return f"Executed: {os.path.basename(self.program_path)}.exe"
                    else:
                        return f"File not found: {self.program_path}"
        except Exception as e:
            return f"Error: {str(e)}"


# Create buttons (7 items)
buttons = []
button_width, button_height = 350, 80
button_margin = 20
start_x = (WIDTH - (button_width * 2 + button_margin)) // 2

# Button positions (2 columns)
positions = [
    (start_x, 280),  # Button 1 (left column) - Moved up a bit
    (start_x, 370),  # Button 2
    (start_x, 460),  # Button 3
    (start_x, 550),  # Button 4

    (start_x + button_width + button_margin, 280),  # Button 5 (right column)
    (start_x + button_width + button_margin, 370),  # Button 6
    (start_x + button_width + button_margin, 460),  # Button 7
]

# Example program names
program_names = [
    "RSIC_T",
    "division_algorithm",
    "D2CA_ANI",
    "parallel_compute",
    "math_art_generator",
    "universe_simulation",
    "quantum_calculator"
]

# Button captions
captions = [
    "Complex network Travers",
    "Division Algorithm",
    "Division by Two Cellular Automata",
    "Parallel Compute",
    "Math Art Generator",
    "Universe Simulation",
    "Quantum Calculator"
]

# Create buttons
for i in range(7):
    x, y = positions[i]
    btn = Button(x, y, button_width, button_height, captions[i], program_names[i])
    buttons.append(btn)

# Status message
status_message = "Ready to launch programs..."

# Main loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):
                        result = button.execute()
                        status_message = result
                        print(f"Attempting to execute: {button.program_path}")

        elif event.type == KEYDOWN:
            if event.key == K_1:
                result = buttons[0].execute()
                status_message = f"Executed: {buttons[0].text}"
            elif event.key == K_2:
                result = buttons[1].execute()
                status_message = f"Executed: {buttons[1].text}"
            elif event.key == K_3:
                result = buttons[2].execute()
                status_message = f"Executed: {buttons[2].text}"
            elif event.key == K_4:
                result = buttons[3].execute()
                status_message = f"Executed: {buttons[3].text}"
            elif event.key == K_5:
                result = buttons[4].execute()
                status_message = f"Executed: {buttons[4].text}"
            elif event.key == K_6:
                result = buttons[5].execute()
                status_message = f"Executed: {buttons[5].text}"
            elif event.key == K_7:
                result = buttons[6].execute()
                status_message = f"Executed: {buttons[6].text}"
            elif event.key == K_ESCAPE:
                running = False
            elif event.key == K_c:
                status_message = "Status cleared"

    # Update button hover states
    for button in buttons:
        button.check_hover(mouse_pos)

    # Drawing
    screen.fill(BACKGROUND_COLOR)

    # Draw title with reduced font
    title_text = title_font.render("Division by Two: Its Own Complete Universe", True, TITLE_COLOR)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 90))  # Moved up a bit
    screen.blit(title_text, title_rect)

    # Draw subtitle with reduced font
    subtitle_text = subtitle_font.render("The Second New Kind of Science", True, SUBTITLE_COLOR)
    subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, 150))  # Moved up
    screen.blit(subtitle_text, subtitle_rect)

    # Draw decorative line under title
    pygame.draw.line(screen, (100, 100, 150), (WIDTH // 2 - 220, 175), (WIDTH // 2 + 220, 175), 2)

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    # ============ LEFT BOX: Presented by ============
    left_box_width = 500
    left_box_height = 200
    left_box_x = 50  # Left side
    left_box_y = HEIGHT - left_box_height - 30  # Bottom left

    # Draw left box
    left_box_rect = pygame.Rect(left_box_x, left_box_y, left_box_width, left_box_height)
    pygame.draw.rect(screen, BOX_COLOR, left_box_rect, border_radius=15)
    pygame.draw.rect(screen, BOX_BORDER_COLOR, left_box_rect, 4, border_radius=15)

    # Draw left box title "Presented by"
    left_box_title = box_title_font.render("Presented by", True, BOX_TITLE_COLOR)
    left_box_title_rect = left_box_title.get_rect(center=(left_box_x + left_box_width // 2, left_box_y + 30))
    screen.blit(left_box_title, left_box_title_rect)

    # Draw decorative line under title in left box
    pygame.draw.line(screen, (150, 200, 255),
                     (left_box_x + left_box_width // 2 - 80, left_box_y + 55),
                     (left_box_x + left_box_width // 2 + 80, left_box_y + 55), 2)

    # Draw names in left box (single column, centered)
    names = [
        "Mohammad Zeynali Azim",
        "Dr. Babak Anari",
        "Dr. Saeid Alikhani",
        "Dr. Bagher Zarei"
    ]

    name_spacing = 35
    names_start_y = left_box_y + 80

    for i, name in enumerate(names):
        name_text = box_text_font.render(name, True, (200, 220, 255))
        name_rect = name_text.get_rect(center=(left_box_x + left_box_width // 2, names_start_y + i * name_spacing))
        screen.blit(name_text, name_rect)

        # Add small decorative dot before each name
        pygame.draw.circle(screen, (100, 200, 255),
                           (left_box_x + left_box_width // 2 - 130, names_start_y + i * name_spacing + 10), 4)

    # ============ RIGHT BOX: How to Run Programs ============
    right_box_width = 500
    right_box_height = 200
    right_box_x = WIDTH - right_box_width - 50  # Right side
    right_box_y = HEIGHT - right_box_height - 30  # Bottom right (same height as left box)

    # Draw right box
    right_box_rect = pygame.Rect(right_box_x, right_box_y, right_box_width, right_box_height)
    pygame.draw.rect(screen, HELP_BOX_COLOR, right_box_rect, border_radius=15)
    pygame.draw.rect(screen, HELP_BOX_BORDER_COLOR, right_box_rect, 4, border_radius=15)

    # Draw right box title "How to Run Programs"
    right_box_title = box_title_font.render("How to Run Programs", True, (255, 180, 100))
    right_box_title_rect = right_box_title.get_rect(center=(right_box_x + right_box_width // 2, right_box_y + 30))
    screen.blit(right_box_title, right_box_title_rect)

    # Draw decorative line under title in right box
    pygame.draw.line(screen, (200, 150, 255),
                     (right_box_x + right_box_width // 2 - 100, right_box_y + 55),
                     (right_box_x + right_box_width // 2 + 100, right_box_y + 55), 2)

    # Draw instructions in right box
    instructions = [
        "• Click buttons to launch programs",
        "• Press 1-7 keys for quick access",
        "• Press C to clear status",
        "• Press ESC to exit",
        "• Programs must be in same folder"
    ]

    instructions_start_y = right_box_y + 75
    instruction_spacing = 28

    for i, instruction in enumerate(instructions):
        inst_color = (220, 200, 255) if i < 4 else (255, 200, 150)  # Different color for last item
        inst_text = help_font.render(instruction, True, inst_color)
        inst_rect = inst_text.get_rect(midleft=(right_box_x + 40, instructions_start_y + i * instruction_spacing))
        screen.blit(inst_text, inst_rect)

        # Add small icon for each instruction
        icon_color = (150, 220, 255) if i < 4 else (255, 180, 100)
        icon_x = right_box_x + 20
        icon_y = instructions_start_y + i * instruction_spacing + 8

        if i == 0:  # Mouse icon
            pygame.draw.circle(screen, icon_color, (icon_x, icon_y), 6)
            pygame.draw.line(screen, icon_color, (icon_x, icon_y - 3), (icon_x + 2, icon_y - 8), 2)
            pygame.draw.line(screen, icon_color, (icon_x, icon_y - 3), (icon_x - 2, icon_y - 8), 2)
        elif i == 1:  # Keyboard icon
            pygame.draw.rect(screen, icon_color, (icon_x - 4, icon_y - 4, 8, 8), 1)
            key_text = help_font.render("1", True, icon_color)
            key_rect = key_text.get_rect(center=(icon_x, icon_y))
            screen.blit(key_text, key_rect)
        elif i == 2:  # C key icon
            pygame.draw.rect(screen, icon_color, (icon_x - 5, icon_y - 5, 10, 10), 1, border_radius=2)
            key_text = help_font.render("C", True, icon_color)
            key_rect = key_text.get_rect(center=(icon_x, icon_y))
            screen.blit(key_text, key_rect)
        elif i == 3:  # ESC key icon
            pygame.draw.rect(screen, icon_color, (icon_x - 7, icon_y - 5, 14, 10), 1, border_radius=2)
            key_text = help_font.render("ESC", True, icon_color)
            key_rect = key_text.get_rect(center=(icon_x, icon_y))
            screen.blit(key_text, key_rect)
        elif i == 4:  # Folder icon
            pygame.draw.rect(screen, icon_color, (icon_x - 8, icon_y - 2, 16, 12), 1)
            pygame.draw.rect(screen, icon_color, (icon_x - 6, icon_y - 5, 12, 3), 1)

    # ============ Status Bar ============
    # Draw status bar at bottom center
    status_bar_width = 600
    status_bar_height = 35
    status_bar_x = (WIDTH - status_bar_width) // 2
    status_bar_y = HEIGHT - 80  # Above the boxes

    # Draw status bar background
    pygame.draw.rect(screen, (30, 45, 65), (status_bar_x, status_bar_y, status_bar_width, status_bar_height),
                     border_radius=8)
    pygame.draw.rect(screen, (80, 120, 160), (status_bar_x, status_bar_y, status_bar_width, status_bar_height), 2,
                     border_radius=8)

    # Draw status message
    status_text = status_font.render(f"Status: {status_message}", True, (200, 220, 100))
    status_rect = status_text.get_rect(center=(WIDTH // 2, status_bar_y + status_bar_height // 2))
    screen.blit(status_text, status_rect)

    # Draw decorative binary pattern at top (centered)
    binary_pattern = "1010 1010 1010 1010"
    pattern_y = 10
    for i, char in enumerate(binary_pattern):
        if char == ' ':
            continue
        color = (80, 160, 220) if char == '1' else (40, 80, 120)
        pattern_x = WIDTH // 2 - 180 + i * 20  # Adjusted spacing
        pygame.draw.rect(screen, color, (pattern_x, pattern_y, 12, 3))

    # Draw current directory info
    current_dir = os.path.basename(os.getcwd())
    dir_text = help_font.render(f"Current Folder: {current_dir}", True, (150, 180, 220))
    dir_rect = dir_text.get_rect(center=(WIDTH // 2, 210))
    screen.blit(dir_text, dir_rect)

    pygame.display.flip()
    clock.tick(60)

# Cleanup
pygame.quit()
sys.exit()