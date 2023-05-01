import pygame
import random
import time
from button import Button 
pygame.init()
clock = pygame.time.Clock()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 550
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN_ON = (0, 255, 0)
GREEN_OFF = (0, 200, 0)
RED_ON = (255, 0, 0)
RED_OFF = (200, 0, 0)
BLUE_ON = (0, 0, 255)
BLUE_OFF = (0, 0, 200)
YELLOW_ON = (255, 255, 0)
YELLOW_OFF = (200, 200, 0)
FONT = pygame.font.SysFont("Arial", 28)

# Pass in respective sounds for each color
GREEN_SOUND = pygame.mixer.Sound("bell1.mp3") 
RED_SOUND = pygame.mixer.Sound("bell2.mp3") 
BLUE_SOUND = pygame.mixer.Sound("bell3.mp3") 
YELLOW_SOUND = pygame.mixer.Sound("bell4.mp3")

# Button Sprite Objects
green = Button(GREEN_ON, GREEN_OFF, GREEN_SOUND, 10, 10)
red = Button(RED_ON, RED_OFF, RED_SOUND, 250, 10)
blue = Button(BLUE_ON, BLUE_OFF, BLUE_SOUND, 10, 250)
yellow = Button(YELLOW_ON, YELLOW_OFF, YELLOW_SOUND, 250, 250)
# Variables
colors = ["green", "red", "blue", "yellow"]
cpu_sequence = []
choice = ""
score = 0
highest_score = 0
game_started = True

def draw_board():
# Call the draw method on all four button objects
    SCREEN.fill(BLACK)
    green.draw(SCREEN)
    red.draw(SCREEN)
    blue.draw(SCREEN)
    yellow.draw(SCREEN)

def cpu_turn():
    choice = random.choice(colors) # pick random color
    cpu_sequence.append(choice) # update cpu sequence
    if choice == "green":
        green.update(SCREEN)
    elif choice == "red":
        red.update(SCREEN)
    elif choice == "blue":
        blue.update(SCREEN)
    elif choice == "yellow":
        yellow.update(SCREEN)
    
def repeat_cpu_sequence():
    SCREEN.blit(FONT.render("Simon says", True, WHITE), (10, 490))
    if(len(cpu_sequence) != 0):
        for color in cpu_sequence:
            if color == "green":
                green.update(SCREEN)
            elif color == "red":
                red.update(SCREEN)
            elif color == "blue":
                blue.update(SCREEN)
            else:
                yellow.update(SCREEN)
            pygame.time.wait(500)

def player_turn():
    timer_rect = pygame.Rect(0, 490, 500, 550) # create an area for the timer  
    turn_time = time.time()
    players_sequence = []
    while time.time() <= turn_time + 3 and len(players_sequence) < len(cpu_sequence):
        # update the timer area every second
        current_time = 3 - (time.time() - turn_time) // 1
        SCREEN.fill((0,0,0), timer_rect) 
        SCREEN.blit(FONT.render("Your turn", True, WHITE), (10, 490))
        SCREEN.blit(FONT.render("Timer: " + str(current_time), True, WHITE), (190, 490))
        SCREEN.blit(FONT.render("Score: " + str(score), True, WHITE), (380, 490))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if green.selected(pos):             # green button was selected
                    green.update(SCREEN)                # illuminate button
                    players_sequence.append("green")    # add to player sequence
                    check_sequence(players_sequence)    # check sequences
                    turn_time = time.time()             # reset timer
                    break
                elif red.selected(pos):             # red button was selected
                    red.update(SCREEN) 
                    players_sequence.append("red") 
                    check_sequence(players_sequence) 
                    turn_time = time.time()
                    break
                elif blue.selected(pos):            # blue button was selected
                    blue.update(SCREEN) 
                    players_sequence.append("blue") 
                    check_sequence(players_sequence) 
                    turn_time = time.time() 
                    break
                elif yellow.selected(pos):          # yellow button was selected
                    yellow.update(SCREEN) 
                    players_sequence.append("yellow") 
                    check_sequence(players_sequence) 
                    turn_time = time.time() 
                    break
            elif event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                quit()
        pygame.display.flip()
    # If player does not select a button within 3 seconds then the game closes
    if not time.time() <= turn_time + 3:
        game_over()

def check_sequence(players_sequence):
    global score
    if players_sequence != cpu_sequence[:len(players_sequence)]:
        game_over()
    elif players_sequence == cpu_sequence:
        score += 1 

def game_over():
    global score, highest_score, game_started
    game_started = False
    if score > highest_score:
        highest_score = score
    pop_up = pygame.Surface((400, 300))
    pop_up_rect = pop_up.get_rect()
    pop_up_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pop_up.fill((0, 0, 0))
    pop_up.blit(FONT.render("YOU SCORED: " + str(score), True, WHITE), (120, 10))
    pop_up.blit(FONT.render("HIGHEST SCORE: " + str(highest_score), True, WHITE), (110, 50))
    pop_up.blit(FONT.render("GAME OVER", True, WHITE), (140, 110))
    reset_button = Button(RED_ON, RED_OFF, RED_SOUND, 180, 290)
    reset_button.image = pygame.Surface((150, 50))
    reset_button.image.fill((255, 0, 0))
    SCREEN.blit(pop_up, pop_up_rect)
    reset_button.draw(SCREEN)
    SCREEN.blit(FONT.render("RESET", True, (255, 255, 255)), (220, 300))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Grab the current position of mouse here
                pos = pygame.mouse.get_pos()
                if reset_button.rect.collidepoint(pos):
                    cpu_sequence.clear()
                    score = 0
                    game_started = True       # restart the game        
                    return
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

def game_start():
    draw_board()            # draws buttons onto pygame screen
    repeat_cpu_sequence()   # repeats cpu sequence if it's not empty
    cpu_turn()              # cpu randomly chooses a new color
    player_turn()           # player tries to recreate cpu sequence
    pygame.time.wait(1000)  # waits one second before repeating cpu sequence
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            quit()
    pygame.display.update()
    if game_started:
        game_start()
    clock.tick(60)
    