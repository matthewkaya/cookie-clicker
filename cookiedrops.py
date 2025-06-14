import pygame
from pygame import *
init()

# Screen setup
width, height = 1000, 700
screen = display.set_mode((width, height))
display.set_caption("Cookie Clicker Deluxe")

# Fonts and Colors
font36 = font.SysFont("Arial", 36)
WHITE, BROWN, BLACK, GREEN, PURPLE, GRAY, LIGHTBLUE = (255,255,255), (210,105,30), (0,0,0), (0,200,0), (200,0,200), (180,180,180), (173,216,230)

# Game Variables
cookie_radius = 100
cookie_x, cookie_y = width//2, height//2
score, click_base = 100000, 1000  # Increased for testing
click_value = 1000
upgrade_cost, upgrade_level = 10, 0
prestige_level, prestige_threshold = 0, 5000

# Buff and Inventory Setup
inventory = {"Quick Fingers": 0, "Adrenaline": 0, "Overdrive": 0}
buff_info = {
    "Quick Fingers": {"multiplier": 2, "duration": 60000, "cost": 5000},
    "Adrenaline": {"multiplier": 3, "duration": 300000, "cost": 20000},
    "Overdrive": {"multiplier": 4, "duration": 600000, "cost": 100000}
}
active_buffs = []
inventory_menu = False
shop_menu = False

clock = time.Clock()
running = True

def draw_text(text, x, y, color=BLACK):
    screen.blit(font36.render(text, True, color), (x, y))

def get_click_value():
    value = click_base
    for name, multiplier, end_time in active_buffs:
        if time.get_ticks() < end_time:
            value *= multiplier
    return value

def update_active_buffs():
    global active_buffs
    active_buffs = [buff for buff in active_buffs if time.get_ticks() < buff[2]]

while running:
    mx, my = mouse.get_pos()
    inventory_button = Rect(20, 600, 200, 40)
    shop_button = Rect(250, 600, 200, 40)
    upgrade_rect = Rect(750, 100, 200, 100)
    prestige_rect = Rect(750, 250, 200, 100)

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
        elif e.type == MOUSEBUTTONDOWN and e.button == 1:
            # Inventory toggle button
            if inventory_button.collidepoint(mx, my):
                inventory_menu = not inventory_menu
                shop_menu = False
                continue
            # Shop toggle button
            if shop_button.collidepoint(mx, my):
                shop_menu = not shop_menu
                inventory_menu = False
                continue

            # Shop interaction
            if shop_menu:
                for i, (name, data) in enumerate(buff_info.items()):
                    buy_rect = Rect(100, 150 + i*90, 150, 40)
                    if buy_rect.collidepoint(mx, my) and score >= data["cost"]:
                        inventory[name] += 1
                        score -= data["cost"]
                continue  # skip other clicks if shop is open

            # Inventory activation
            if inventory_menu:
                for i, (name, data) in enumerate(buff_info.items()):
                    act_rect = Rect(400, 180 + i*90, 150, 40)
                    if act_rect.collidepoint(mx, my) and inventory[name] > 0:
                        inventory[name] -= 1
                        found = False
                        for buff in active_buffs:
                            if buff[0] == name:
                                buff[2] += data["duration"]
                                found = True
                                break
                        if not found:
                            active_buffs.append([name, data["multiplier"], time.get_ticks() + data["duration"]])
                continue  # skip other clicks if inventory is open

            # Cookie clicking
            dx, dy = mx - cookie_x, my - cookie_y
            if dx*dx + dy*dy <= cookie_radius**2:
                score += get_click_value()

            # Upgrade
            if upgrade_rect.collidepoint(mx, my) and score >= upgrade_cost:
                score -= upgrade_cost
                upgrade_level += 1
                click_base += 1
                upgrade_cost *= 2

            # Prestige
            if score >= prestige_threshold and prestige_rect.collidepoint(mx, my):
                prestige_level += 1
                click_base = prestige_level + 1
                score = 0
                upgrade_level = 0
                upgrade_cost = 10
                # Do NOT clear active_buffs or inventory

    update_active_buffs()

    # Draw base UI
    screen.fill(WHITE)
    draw.circle(screen, BROWN, (cookie_x, cookie_y), cookie_radius)
    draw_text(f"Score: {score}", 20, 20)
    draw_text(f"Click: +{get_click_value()}", 20, 60)
    draw_text(f"Prestige: {prestige_level}", 20, 100)

    draw.rect(screen, GREEN, upgrade_rect)
    draw_text("Upgrade", 770, 120)
    draw_text(f"Cost: {upgrade_cost}", 770, 160)

    if score >= prestige_threshold:
        draw.rect(screen, PURPLE, prestige_rect)
        draw_text("Prestige", 770, 270, WHITE)
        draw_text("Reset + Boost", 755, 310, WHITE)

    draw.rect(screen, GRAY, inventory_button)
    draw_text("Toggle Inventory (i)", 25, 605)

    draw.rect(screen, LIGHTBLUE, shop_button)
    draw_text("Toggle Shop (s)", 260, 605)

    # Active Buffs Display
    draw_text("Active Buffs:", 20, 150)
    for i, (name, mult, end) in enumerate(active_buffs):
        time_left = (end - time.get_ticks()) // 1000
        draw_text(f"{name} x{mult} ({time_left}s)", 20, 180 + i*30)

    # Inventory Menu
    if inventory_menu:
        draw.rect(screen, GRAY, (350, 100, 600, 400))
        draw_text("Inventory", 370, 110)
        for i, (name, data) in enumerate(buff_info.items()):
            draw_text(f"{name}: {inventory[name]}", 370, 150 + i*90)
            act_rect = Rect(400, 180 + i*90, 150, 40)
            draw.rect(screen, GREEN, act_rect)
            draw_text("Activate", 405, 185 + i*90)

    # Shop Menu
    if shop_menu:
        draw.rect(screen, LIGHTBLUE, (80, 100, 300, 400))
        draw_text("Shop", 100, 110)
        for i, (name, data) in enumerate(buff_info.items()):
            draw_text(f"{name} - ${data['cost']}", 100, 130 + i*90)
            buy_rect = Rect(100, 150 + i*90, 150, 40)
            draw.rect(screen, GREEN, buy_rect)
            draw_text("Buy", 105, 155 + i*90)

    display.flip()
    clock.tick(60)

quit()