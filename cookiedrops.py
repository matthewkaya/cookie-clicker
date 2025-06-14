"""
Cookie Drops Game
---------------
A cookie clicker game with falling cookie drops that players can click to earn points.
This game demonstrates the use of Pygame for graphics, user input handling,
and game mechanics.

Assignment Requirements:
- Graphics-based game (1000x700)
- Uses Pygame drawing functions
- Implements various programming control structures (loops, conditionals)
- Allows for user input (mouse clicks)
- Uses modular programming (functions)
- Includes proper documentation
"""

import pygame
from pygame import *
import random  # For generating random cookie drops
import os  # For file path handling
import sys  # For system-specific parameters

# Initialize pygame with specific options to avoid audio warnings
pygame.init()
# Initialize sound with a fallback to avoid ALSA errors
try:
    pygame.mixer.init()
except pygame.error:
    # If mixer initialization fails, continue without sound
    print("Sound initialization failed. Game will run without sound.")
    pygame.mixer.quit()

# Screen setup
width, height = 1000, 700
screen = display.set_mode((width, height))
display.set_caption("Cookie Drops")

# Fonts and Colors
font36 = font.SysFont("Arial", 36)
font24 = font.SysFont("Arial", 24)
WHITE = (255, 255, 255)
BROWN = (210, 105, 30)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
PURPLE = (200, 0, 200)
GRAY = (180, 180, 180)
LIGHTBLUE = (173, 216, 230)
GOLD = (255, 215, 0)

# Set up background
background = pygame.Surface((width, height))
background.fill(WHITE)

# Game Variables
cookie_radius = 60
main_cookie_x, main_cookie_y = width // 2, height // 2
score = 0  # Start with 0 score
click_base = 1  # Start with 1 point per click
click_value = 1
upgrade_cost = 10
upgrade_level = 0
prestige_level = 0
prestige_threshold = 5000

# Falling Cookies setup
class CookieDrop:
    def __init__(self):
        self.radius = random.randint(20, 40)
        self.x = random.randint(self.radius, width - self.radius)
        self.y = -self.radius
        self.speed = random.uniform(1, 5)
        self.color = (
            random.randint(180, 210),  # R - shades of brown
            random.randint(80, 140),   # G
            random.randint(20, 50)     # B
        )
        self.active = True
        self.value = random.randint(5, 20) * (prestige_level + 1)
        
    def update(self):
        self.y += self.speed
        # Check if cookie has fallen off the screen
        if self.y > height + self.radius:
            self.active = False
            
    def draw(self):
        # Draw the cookie
        draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Add chocolate chips
        for _ in range(3):
            chip_x = self.x + random.randint(-self.radius//2, self.radius//2)
            chip_y = self.y + random.randint(-self.radius//2, self.radius//2)
            # Ensure chips are inside the cookie
            if (chip_x - self.x)**2 + (chip_y - self.y)**2 < (self.radius*0.7)**2:
                draw.circle(screen, (50, 25, 0), (int(chip_x), int(chip_y)), self.radius//5)
                
    def is_clicked(self, pos):
        mx, my = pos
        distance = ((self.x - mx)**2 + (self.y - my)**2)**0.5
        return distance <= self.radius

# Visual effect for cookie clicks
class ClickEffect:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.lifetime = 30  # frames
        self.color = GOLD
        self.font = font24
        
    def update(self):
        self.lifetime -= 1
        self.y -= 2  # Move upward
        
    def draw(self):
        # Fade out as lifetime decreases
        alpha = int(255 * (self.lifetime / 30))
        text = f"+{self.value}"
        text_surface = self.font.render(text, True, self.color)
        # Create a temporary surface with alpha channel
        alpha_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
        alpha_surface.fill((255, 255, 255, alpha))
        # Blit with alpha blending
        text_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(text_surface, (self.x - text_surface.get_width() // 2, self.y))

# List to store click effects
click_effects = []

# Create a list to store falling cookies
falling_cookies = []
cookie_spawn_timer = 0
cookie_spawn_interval = 1000  # Milliseconds between cookie spawns

# Buff and Inventory Setup
inventory = {"Quick Fingers": 0, "Adrenaline": 0, "Overdrive": 0}
buff_info = {
    "Quick Fingers": {"multiplier": 2, "duration": 10000, "cost": 50},
    "Adrenaline": {"multiplier": 3, "duration": 15000, "cost": 200},
    "Overdrive": {"multiplier": 4, "duration": 20000, "cost": 500}
}
active_buffs = []
inventory_menu = False
shop_menu = False

# Setup game clock and running state
clock = time.Clock()
running = True
last_time = pygame.time.get_ticks()

# Function definitions
def draw_text(text, x, y, font_size=36, color=BLACK):
    """Draw text on the screen with the specified font and color"""
    if font_size == 36:
        text_surface = font36.render(text, True, color)
    else:
        text_surface = font24.render(text, True, color)
    screen.blit(text_surface, (x, y))

def get_click_value():
    """Calculate current click value based on active buffs"""
    value = click_base
    for name, multiplier, end_time in active_buffs:
        if time.get_ticks() < end_time:
            value *= multiplier
    return value
    # Draw chocolate chips
    for _ in range(5):
        chip_x = main_cookie_x + random.randint(-cookie_radius//2, cookie_radius//2)
        chip_y = main_cookie_y + random.randint(-cookie_radius//2, cookie_radius//2)
        # Ensure chips are inside the cookie
        if (chip_x - main_cookie_x)**2 + (chip_y - main_cookie_y)**2 < (cookie_radius*0.7)**2:
            draw.circle(screen, (50, 25, 0), (int(chip_x), int(chip_y)), cookie_radius//5)

def draw_ui():
    """Draw the game UI elements"""
    # Draw score and stats
    draw_text(f"Score: {score}", 20, 20)
    draw_text(f"Click: +{get_click_value()}", 20, 60)
    draw_text(f"Prestige: {prestige_level}", 20, 100)

    # Draw upgrade button
    draw.rect(screen, GREEN, upgrade_rect)
    draw_text("Upgrade", 770, 120)
    draw_text(f"Cost: {upgrade_cost}", 770, 160, 24)

    # Draw prestige button if score is high enough
    if score >= prestige_threshold:
        draw.rect(screen, PURPLE, prestige_rect)
        draw_text("Prestige", 770, 270, 36, WHITE)
        draw_text("Reset + Boost", 755, 310, 24, WHITE)

    # Draw inventory and shop buttons
    draw.rect(screen, GRAY, inventory_button)
    draw_text("Inventory (i)", 40, 605)

    draw.rect(screen, LIGHTBLUE, shop_button)
    draw_text("Shop (s)", 280, 605)

    # Display active buffs
    draw_text("Active Buffs:", 20, 150)
    for i, (name, mult, end) in enumerate(active_buffs):
        time_left = (end - time.get_ticks()) // 1000
        draw_text(f"{name} x{mult} ({time_left}s)", 20, 180 + i*30, 24)

def draw_inventory():
    """Draw the inventory menu if it's open"""
    if inventory_menu:
        draw.rect(screen, GRAY, (350, 100, 600, 400))
        draw_text("Inventory", 370, 110)
        for i, (name, count) in enumerate(inventory.items()):
            draw_text(f"{name}: {count}", 370, 150 + i*90)
            if count > 0:
                act_rect = Rect(400, 180 + i*90, 150, 40)
                draw.rect(screen, GREEN, act_rect)
                draw_text("Activate", 405, 185 + i*90, 24)

def draw_shop():
    """Draw the shop menu if it's open"""
    if shop_menu:
        draw.rect(screen, LIGHTBLUE, (80, 100, 300, 400))
        draw_text("Shop", 100, 110)
        for i, (name, data) in enumerate(buff_info.items()):
            draw_text(f"{name} - {data['cost']}", 100, 130 + i*90)
            buy_rect = Rect(100, 150 + i*90, 150, 40)
            draw.rect(screen, GREEN, buy_rect)
            draw_text("Buy", 105, 155 + i*90, 24)

def handle_shop_click(pos):
    """Handle clicks in the shop menu"""
    global score
    mx, my = pos
    for i, (name, data) in enumerate(buff_info.items()):
        buy_rect = Rect(100, 150 + i*90, 150, 40)
        if buy_rect.collidepoint(mx, my) and score >= data["cost"]:
            inventory[name] += 1
            score -= data["cost"]

def handle_inventory_click(pos):
    """Handle clicks in the inventory menu"""
    mx, my = pos
    for i, (name, count) in enumerate(inventory.items()):
        act_rect = Rect(400, 180 + i*90, 150, 40)
        if act_rect.collidepoint(mx, my) and count > 0:
            data = buff_info[name]
            inventory[name] -= 1
            found = False
            for buff in active_buffs:
                if buff[0] == name:
                    buff[2] += data["duration"]
                    found = True
                    break
            if not found:
                active_buffs.append([name, data["multiplier"], time.get_ticks() + data["duration"]])

def handle_cookie_drop_clicks(pos):
    """Handle clicks on falling cookies"""
    global score
    for cookie in falling_cookies[:]:  # Create a copy to avoid modification during iteration
        if cookie.is_clicked(pos):
            score += cookie.value * get_click_value()
            cookie.active = False  # Remove the cookie
            return True  # Return True if a cookie was clicked
    return False

# Main game loop
while running:
    current_time = pygame.time.get_ticks()
    delta_time = current_time - last_time
    last_time = current_time
    
    # Update cookie spawn timer
    cookie_spawn_timer += delta_time
    if cookie_spawn_timer >= cookie_spawn_interval:
        spawn_cookie_drop()
        cookie_spawn_timer = 0
        # Decrease spawn interval as game progresses, but not below 200ms
        cookie_spawn_interval = max(200, 1000 - (upgrade_level * 50))
    
    # Get mouse position for UI interaction
    mx, my = mouse.get_pos()
    
    # Define UI rectangles
    inventory_button = Rect(20, 600, 200, 40)
    shop_button = Rect(250, 600, 200, 40)
    upgrade_rect = Rect(750, 100, 200, 100)
    prestige_rect = Rect(750, 250, 200, 100)

    # Event handling
    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.key == K_i:
                inventory_menu = not inventory_menu
                shop_menu = False
            elif e.key == K_s:
                shop_menu = not shop_menu
                inventory_menu = False
        elif e.type == MOUSEBUTTONDOWN and e.button == 1:  # Left mouse button
            # Handle UI button clicks
            if inventory_button.collidepoint(mx, my):
                inventory_menu = not inventory_menu
                shop_menu = False
                continue
            if shop_button.collidepoint(mx, my):
                shop_menu = not shop_menu
                inventory_menu = False
                continue

            # Handle shop menu clicks
            if shop_menu:
                handle_shop_click((mx, my))
                continue

            # Handle inventory menu clicks
            if inventory_menu:
                handle_inventory_click((mx, my))
                continue

            # Handle falling cookie clicks
            if handle_cookie_drop_clicks((mx, my)):
                continue

            # Handle main cookie clicks
            dx, dy = mx - main_cookie_x, my - main_cookie_y
            if dx*dx + dy*dy <= cookie_radius**2:
                score += get_click_value()

            # Handle upgrade button clicks
            if upgrade_rect.collidepoint(mx, my) and score >= upgrade_cost:
                score -= upgrade_cost
                upgrade_level += 1
                click_base += 1
                upgrade_cost = int(upgrade_cost * 1.5)  # Increase cost by 50% each time

            # Handle prestige button clicks
            if score >= prestige_threshold and prestige_rect.collidepoint(mx, my):
                prestige_level += 1
                click_base = prestige_level + 1
                score = 0
                upgrade_level = 0
                upgrade_cost = 10
                # Do NOT clear active_buffs or inventory

    # Update game state
    update_active_buffs()
    update_cookie_drops()

    # Draw game elements
    screen.fill(WHITE)
    draw_main_cookie()
    draw_cookie_drops()
    draw_ui()
    draw_inventory()
    draw_shop()

    # Update display
    display.flip()
    clock.tick(60)  # 60 frames per second

# Clean up and exit
pygame.quit()