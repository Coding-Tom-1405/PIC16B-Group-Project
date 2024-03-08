import pygame
import random
from glob import glob
import os

# all the possible positions for the numbers
coord = [(x, y) for x in range(1, 10) for y in range(1, 10)] 
original_coord = coord[:]

def game_init():
    global screen, font

    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Chimp Memory Test")
    font = pygame.font.SysFont("Times New Roman", 35)
 
    # Changing surface color
    screen.fill((0,0,255))
#     pygame.display.flip()


class Square(pygame.sprite.Sprite):
     
    def __init__(self, number, make_image=True):
        super(Square, self).__init__()
        self.number = number
        if make_image:
            self.make_image()
        
        
    def update(self):
        
        self.make_image()
        screen.blit(self.image, (self.x, self.y))

        
    def random_coord(self):
        
        global coord  # Access the global pos list

        if not coord:
            # Regenerate pos list if it's empty
            coord.extend(original_coord)
        coordinates = random.choice(coord)
        x, y = coordinates
        coord.remove(coordinates)  # Remove the chosen position from the list
        x = x * 80
        y = y * 80
        return x, y
    
    def make_image(self):
        global font
        self.x, self.y = self.random_coord()
        self.image = pygame.Surface((80, 80))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.number = str(self.number)
        self.text = font.render(self.number, 1, (0, 0, 0))
        text_rect = self.text.get_rect(center=(80 // 2, 80 // 2))
        self.image.blit(self.text, text_rect)

square_group = pygame.sprite.Group()
num_list = []
level = 1
incorrect_guesses = 0
# This covers the numbers...
bgd = pygame.Surface((80, 80))
# sprite_coordinate = []

def hide_cards():
    for sprite in square_group:
        bgd.fill((255, 255, 255))
        sprite.image.blit(bgd, (0, 0))
def reset_coord():
    global coord, original_coord
    coord = original_coord[:]  # Reset pos to its original state        



def memory(sprite):
    global num_list, level, timer_on, max_timer, cards_visible, incorrect_guesses, loop
    # Check the collision only when conter is off
    x, y = pygame.mouse.get_pos() 
    if sprite.rect.collidepoint(x, y):
#         play()#"click")
        num_list.append(sprite.number)
        sprite.rect = pygame.Rect(-80, -80, 80, 80)

        # Check if you are wrong as you type
        if sprite.number != str(len(num_list)):
            print(str(level))
            print("incorrect")
            reset_coord()
            incorrect_guesses += 1
            if incorrect_guesses >= 3:
                loop = 0  # Terminate the game loop
            num_list = []
            timer_on = 1
            square_group.update()
            screen.fill((255, 0, 0))  # Fill the screen with red color
            pygame.display.flip()  # Update the display
            pygame.time.wait(500)  # Wait for 500 milliseconds
  




    if len(num_list) == len(square_group):
        # =========================== YOU GUESSED ========== 
        win = num_list == [str(squares.number) for squares in square_group]
        if win:   
            print(str(level))
            level += 1
            print("correct")
            reset_coord()
            
            num_list = []
            square_group.add(Square(len(square_group) + 1, make_image = False))
            timer_on = 1
            max_timer += 10
            cards_visible = 1
            bgd.fill((255,0,0))
            screen.fill((0, 255, 0))  # Fill the screen with green color
            pygame.display.flip()  # Update the display to show the green screen
            pygame.time.wait(500)  # Wait for 200 milliseconds
            screen.fill((0, 0, 0))  # Fill the screen with black color again
            pygame.display.flip()  # Update the display to show the black screen
            
            
        else:
            print(str(level))
            print("incorrect")
            reset_coord()
            incorrect_guesses += 1
            if incorrect_guesses >= 3:
                loop = 0  # Terminate the game loop
            num_list = []
            timer_on = 1
            cards_visible = 1
            screen.fill((255, 0, 0))  # Fill the screen with red color
           
        square_group.update()
        print("-"*25)
        screen.fill((0, 0, 0))  # Fill the screen with black color
        


######################
#     sound          #
######################
def init():
    "Initializing pygame and mixer"
#     pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
#     pygame.mixer.quit()
#     pygame.mixer.init(22050, -16, 2, 512)
#     pygame.mixer.set_num_channels(32)
    # Load all sounds
#     lsounds = glob("sounds\\*.mp3")
#     print(lsounds)
#     # Dictionary with all sounds, keys are the name of wav
#     sounds = {}
#     for sound in lsounds:
#         sounds[sound.split("\\")[1][:-4]] = pygame.mixer.Sound(f"{sound}")
#     return sounds
# =========================== ([ sounds ]) ============

# sounds = init()

# base = pygame.mixer.music
# def soundtrack(filename, stop=0):
#     "This load a base from sounds directory"
#     base.load(filename)
#     if stop == 1:
#         base.stop()
#     else:
#         base.play(-1)

#def play():#sound):
#     pygame.mixer.Sound.play(sounds[sound])
    return None
def squares_init():
    for i in range(1, 4):
        square_group.add(Square(i))

counter = 0
timer_on = 1
max_timer = 200
cards_visible = 1

def get_maxlevel() -> int:
    filename = "maxlevel.txt"
    if filename in os.listdir():
        with open(filename, "r") as file:
            leader = file.read()
            if leader == "":
                maxlevel = 0
            else:
                maxlevel = int(leader)
    else:
        maxlevel = 0
    return maxlevel

def set_maxlevel(maxlevel) -> None:
    with open("maxlevel.txt", "w") as file:
        file.write(str(maxlevel))

def update_maxlevel(level):
    maxlevel = get_maxlevel()
    if level > maxlevel:
        set_maxlevel(level)

def main():
    global timer_on, counter, max_timer, cards_visible, loop

    game_init()
    squares_init()
    clock = pygame.time.Clock()

    loop = 1
    # pygame.mouse.set_visible(False)
#     soundtrack("sounds/soave.ogg")
    while loop:
        screen.fill((0,0,255))
        text = font.render("Level: " + str(level), 1, (255, 255, 255))
        screen.blit(text, (0, 0))
        if timer_on:
            text = font.render(" Time: " + str(max_timer - counter), 1, (255, 255, 255))
            screen.blit(text, (200, 0))
            counter += 1
#             if counter % 4 == 0:
#                 play()#"click")
        for event in pygame.event.get():
            # ========================================= QUIT
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    loop = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Click mouse and stop the timer and hide the cards
                for squares in square_group:
                    if squares.rect.collidepoint(event.pos):
                        hide_cards()
                        cards_visible = 0
                        timer_on = 0
                        counter = 0
                        memory(squares)    


        square_group.draw(screen)
        # Hides the number...
        if counter == max_timer:
#             hide_cards()
            counter = 0
            timer_on = 0

                # pygame.mouse.set_visible(True)
        pygame.display.update()
        clock.tick(20)
                
    pygame.quit()

    
main()
update_maxlevel(level)
