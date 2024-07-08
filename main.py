import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
MAX_RESOLUTION = pygame.display.list_modes()[0]  # Get maximum available resolution
SCREEN_WIDTH, SCREEN_HEIGHT = MAX_RESOLUTION
GRAVITY = 0.25
BIRD_SPEED = 4  # Initial game speed
INIT_JUMP_VEL = -6  # Initial jump velocity
MAX_JUMP_VEL = -8  # Maximum jump velocity (decreased)
JUMP_ACCEL = 0.4  # Acceleration due to jump (decreased)
PIPE_GAP = 200  # Increased gap between upper and lower pipes
PIPE_WIDTH = 70
PIPE_HEIGHT = 300  # Adjusted pipe height
PIPE_DISTANCE = 300  # Increased distance between adjacent pipes
FPS = 60
FONT = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)

# Game classes
class Bird:
    def __init__(self):
        self.x, self.y, self.velocity = 50, SCREEN_HEIGHT // 2, INIT_JUMP_VEL
        self.image = pygame.image.load('bird.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))  # Resize bird image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def flap(self):
        if self.velocity < MAX_JUMP_VEL:
            self.velocity -= JUMP_ACCEL  # Decrease jump acceleration (smaller jumps)
        else:
            self.velocity = MAX_JUMP_VEL

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, pipes):
        if self.y > SCREEN_HEIGHT or self.y < 0:
            return True
        for pipe in pipes:
            if self.rect.colliderect(pipe.upper_rect) or self.rect.colliderect(pipe.lower_rect):
                return True
        return False

class Pipe:
    def __init__(self, x):
        self.x, self.y = x, random.randint(-PIPE_HEIGHT // 2, SCREEN_HEIGHT // 2)
        self.upper_pipe = pygame.image.load('pipe.png').convert_alpha()
        self.upper_pipe = pygame.transform.scale(self.upper_pipe, (PIPE_WIDTH, PIPE_HEIGHT))  # Resize pipe image
        self.lower_pipe = pygame.transform.flip(self.upper_pipe, False, True)
        self.upper_rect = self.upper_pipe.get_rect(topleft=(self.x, self.y))
        self.lower_rect = self.lower_pipe.get_rect(topleft=(self.x, self.y + PIPE_HEIGHT + PIPE_GAP))
        self.passed = False  # Flag to track if bird has passed this pipe

    def update(self):
        self.x -= BIRD_SPEED
        self.upper_rect = self.upper_pipe.get_rect(topleft=(self.x, self.y))
        self.lower_rect = self.lower_pipe.get_rect(topleft=(self.x, self.y + PIPE_HEIGHT + PIPE_GAP))

    def draw(self, screen):
        screen.blit(self.upper_pipe, self.upper_rect)
        screen.blit(self.lower_pipe, self.lower_rect)

    def offscreen(self):
        return self.x < -PIPE_WIDTH

# Initialize game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)  # Set fullscreen mode
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

bird, pipes, score = Bird(), [], 0
background = pygame.image.load('background.png').convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize background image
game_over_img = pygame.image.load('gameover.png').convert_alpha()

# Functions
def generate_pipe():
    pipes.append(Pipe(SCREEN_WIDTH + PIPE_DISTANCE))  # Increased distance between pipes

def draw_score():
    screen.blit(FONT.render(f'Score: {score}', True, WHITE), (10, 10))

def game_over():
    screen.blit(game_over_img, (50, SCREEN_HEIGHT // 2 - 100))
    pygame.display.update()
    pygame.time.delay(2000)
    main()

def quit_game():
    pygame.quit()
    sys.exit()

# Main game loop
def main():
    global score
    bird.__init__()
    pipes.clear()
    score = 0
    frame_count = 0  # Keep track of frames
    while True:
        screen.blit(background, (0, 0))
        bird.update()
        bird.draw(screen)
        [pipe.update() or pipe.draw(screen) for pipe in pipes]
        draw_score()
        if bird.check_collision(pipes): game_over()
        
        # Check if bird passed a pipe
        for pipe in pipes:
            if not pipe.passed and pipe.x + PIPE_WIDTH // 2 < bird.x:
                pipe.passed = True
                score += 1
        
        pygame.display.update()
        clock.tick(FPS)
        frame_count += 1
        if frame_count % (FPS * 5) == 0:  # Increase speed every 5 seconds
            global BIRD_SPEED
            BIRD_SPEED += 1
        [generate_pipe() for _ in range(1) if not pipes or pipes[-1].x < SCREEN_WIDTH - PIPE_DISTANCE]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
                elif event.key == pygame.K_ESCAPE:
                    quit_game()

if __name__ == '__main__':
    main()
