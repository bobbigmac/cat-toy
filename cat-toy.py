import pygame
import sys
import random
import time
import math # Added for math.sin

# Initialize Pygame
pygame.init()

# Set up fullscreen display (borderless fullscreen)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
pygame.display.set_caption("Cat Playtime")
width, height = screen.get_size()

# Natural cat-friendly palette (RGB) - inspired by nature and cat vision
palette = [
    (139, 69, 19),    # Saddle Brown - earth tones
    (34, 139, 34),    # Forest Green - natural green
    (160, 82, 45),    # Sienna - warm brown
    (255, 140, 0),    # Dark Orange - sunset orange
    (128, 128, 0),    # Olive - natural olive
    (210, 180, 140),  # Tan - warm neutral
    (255, 215, 0),    # Gold - warm yellow
    (178, 34, 34),    # Firebrick - deep red
    (85, 107, 47),    # Dark Olive Green - forest
    (205, 133, 63)    # Peru - warm brown
]

# Shape class
class Shape:
    def __init__(self, shape_type):
        self.shape_type = shape_type
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.vx = (random.random() - 0.5) * 15 * energy  # Much faster initial velocity
        self.vy = (random.random() - 0.5) * 15 * energy
        self.color = random.choice(palette)
        self.base_size = random.randint(50, 120)  # Bigger random base size
        self.size = self.base_size
        self.size_oscillation = 0  # For size animation
        self.oscillation_speed = random.uniform(0.1, 0.3)  # Faster oscillation
        self.twitch_timer = 0  # For sudden twitchy movements
        self.twitch_cooldown = 0  # Cooldown after twitching
        self.twitch_cooldown_duration = random.uniform(3.0, 8.0)  # Random cooldown duration
        self.has_twitched = False  # Track if shape has twitched recently

        # Define points for polygon-based shapes (relative to center)
        if shape_type == "triangle":
            self.points = [(0, -20), (20, 20), (-20, 20)]
        elif shape_type == "star":
            self.points = [
                (0, -30), (10, -10), (30, -10), (15, 5), (20, 25),
                (0, 15), (-20, 25), (-15, 5), (-30, -10), (-10, -10)
            ]
        else:
            self.points = None

    def update_position(self, dt):
        # Update cooldown timer
        if self.twitch_cooldown > 0:
            self.twitch_cooldown -= dt  # Use actual delta time
            if self.twitch_cooldown <= 0:
                self.has_twitched = False  # Reset twitch flag
        
        # Only allow twitching if not in cooldown
        if not self.has_twitched and self.twitch_cooldown <= 0:
            self.twitch_timer += dt
            if self.twitch_timer >= 1.0:  # Check every second
                # Random chance to twitch
                if random.random() < 0.4:  # 40% chance
                    self._perform_twitch()
                self.twitch_timer = 0
        
        self.x += self.vx  # Don't multiply by dt - velocity is already in pixels per frame
        self.y += self.vy
        
        # Update size oscillation with more twitchy behavior
        self.size_oscillation += self.oscillation_speed * dt
        movement_factor = (abs(self.vx) + abs(self.vy)) / 4.0
        
        # Add random spikes for surprise
        random_spike = random.random() * 0.3  # 30% chance of size spike
        if random_spike < 0.1:  # 10% chance of big spike
            size_variation = random.uniform(20, 40)
        else:
            size_variation = math.sin(self.size_oscillation) * movement_factor * 25
        
        self.size = max(15, self.base_size + size_variation)  # Bigger minimum size
        
        if self.x < 0 or self.x > width:
            self.vx *= -1
        if self.y < 0 or self.y > height:
            self.vy *= -1

    def _perform_twitch(self):
        """Perform a twitch movement"""
        self.vx += (random.random() - 0.5) * 20 * energy  # Much bigger twitch velocity changes
        self.vy += (random.random() - 0.5) * 20 * energy
        # Clamp velocity to reasonable range
        self.vx = max(-25 * energy, min(25 * energy, self.vx))  # Higher max velocity
        self.vy = max(-25 * energy, min(25 * energy, self.vy))
        self.has_twitched = True
        self.twitch_cooldown = self.twitch_cooldown_duration

    def force_twitch(self):
        """Force a twitch (called by keypress/touch events)"""
        if self.twitch_cooldown <= 0:
            self._perform_twitch()

    def draw(self, surface):
        if self.shape_type == "circle":
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size // 2))
        elif self.shape_type == "square":
            rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
            pygame.draw.rect(surface, self.color, rect)
        elif self.shape_type in ["triangle", "star"]:
            # Scale points based on current size
            scale_factor = self.size / self.base_size
            scaled_points = [(px * scale_factor, py * scale_factor) for px, py in self.points]
            abs_points = [(self.x + px, self.y + py) for px, py in scaled_points]
            pygame.draw.polygon(surface, self.color, abs_points)

    def change_color(self):
        self.color = random.choice(palette)

    def change_speed(self):
        self.vx = (random.random() - 0.5) * 15 * energy  # Much faster speed changes
        self.vy = (random.random() - 0.5) * 15 * energy

# Global variables
shapes = []
energy = 1.0
activity_count = 0
last_activity_time = time.time()
debounce_time = 0.3  # seconds
last_key_time = 0
bg_color = random.choice(palette)
shape_types = ["circle", "square", "triangle", "star"]

# Initial shapes
for _ in range(5):
    shapes.append(Shape(random.choice(shape_types)))

# Font for exit info
font = pygame.font.SysFont(None, 24)

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    current_time = time.time()
    dt = clock.tick(60) / 1000.0  # Get actual delta time in seconds

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Ignore QUIT event to prevent easy close
            continue
        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            # Check for exit combo: Ctrl + Shift + W
            if event.key == pygame.K_w and (mods & pygame.KMOD_CTRL) and (mods & pygame.KMOD_SHIFT):
                running = False
                break

            # Ignore F11 (browser habit, but allow if wanted)
            if event.key == pygame.K_F11:
                continue

            # Debounce and handle other keypresses
            if current_time - last_key_time >= debounce_time:
                last_key_time = current_time

                # Random action
                actions = [
                    lambda: shapes.append(Shape(random.choice(shape_types))),  # Add shape
                    lambda: shapes.pop(random.randrange(len(shapes))) if shapes else None,  # Remove shape
                    lambda: [s.change_color() for s in shapes],  # Change colors
                    lambda: [s.change_speed() for s in shapes],  # Change speeds
                    lambda: globals().update({'bg_color': random.choice(palette)}),  # Change background
                    lambda: [s.force_twitch() for s in shapes]  # Force twitches on all shapes
                ]
                random.choice(actions)()

                # Track activity
                activity_count += 1

    # Update energy every second
    if current_time - last_activity_time > 1:
        energy = max(1.0, activity_count / 5)
        activity_count = 0
        last_activity_time = current_time
        # Update all speeds with new energy
        for s in shapes:
            s.change_speed()

    # Update shape positions with proper delta time
    for s in shapes:
        s.update_position(dt)

    # Draw everything
    screen.fill(bg_color)
    for s in shapes:
        s.draw(screen)

    # Draw exit info with semi-transparent background
    text = font.render("Press Ctrl+Shift+W to exit", True, (0, 0, 0))
    text_bg = pygame.Surface((text.get_width() + 10, text.get_height() + 10))
    text_bg.fill((255, 255, 255))
    text_bg.set_alpha(178)  # ~70% opacity
    screen.blit(text_bg, (5, 5))
    screen.blit(text, (10, 10))

    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()
