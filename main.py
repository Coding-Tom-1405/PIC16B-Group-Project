# Import necessary packages
import pygame
import random
import os
import csv
import asyncio
# import requests 
# import json

coord = [(x, y) for x in range(1, 10) for y in range(1, 10)] # Setting the position grid for our squares
original_coord = coord[:] # Creating replica of coord to update coord after each level
square_group = pygame.sprite.Group() # Creating the grouping of the squares
num_list = [] # Creating list to append the numbers of each square
level = 1 # Setting level value
incorrect_guesses = 0 # Setting amount of incorrect guesses currently made
difficulty_file = "/Users/owensun/Downloads/PIC16B-Group-Project-main 5/game_setting.csv"
#difficulty = 1
timer_on = 1


with open(difficulty_file, 'r') as file:
     last_line = file.readlines()[-1]
     difficulty = int(last_line.split(',')[0])
     if last_line.split(',')[1] == 'timer\n' :
         timer_chosen = 1
     else :
         timer_chosen = 0

def game_init():
    """
    Initializing game
    """
    global font, screen
    pygame.init()                                                  # Initializing pygame modules
    screen = pygame.display.set_mode((800, 800))                   # Setting screen size
    pygame.display.set_caption("Chimp Test")                       # Setting game name
    font = pygame.font.SysFont("Times New Roman", 50)              # Setting general text font and size
    screen.fill((0, 0, 255))                                       # Setting background color

class Square(pygame.sprite.Sprite): 
    """
    Class representing Square object in the game
    """
    def __init__(self, number, make_square=True):
        """
        Initializing Square object with given number

        Args:
            number (int): Number associated with square
            make_square (bool): Flag indicating whether to create the squares; True default

        Returns:
            None
        """
        super(Square, self).__init__()
        self.number = number
        if make_square:
            self.make_square()

    def update(self): 
        """
        Updating the appearance of the square on the screen 
        by using the 'make_square' method and then blitting image on screen
        """
        self.make_square()
        screen.blit(self.image, (self.x, self.y))     # Blitting square onto screen at its allocated coordinate

    def random_coord(self): 
        """
        Generating random coordinates for each square
        """
        global coord
        if not coord:                                      # Checking if coord is empty
            coord.extend(original_coord)                   # Refilling the list
        coordinates = random.choice(coord)                 # Choosing random coordinates
        coord.remove(coordinates)                          # Removing the chosen coordinates to prevent repeats
        x, y = coordinates 
        return x * 80, y * 80                              # Return scaled coordinates to get 80 x 80 square

    def make_square(self):
        """
        Creating the graphical representation of the squares 
        using 'random_coord' method to assign squares the coordinates
        """
        global font
        self.x, self.y = self.random_coord()                       # Assigning the square a coordinate
        self.image = pygame.Surface((80, 80))                      # Creating a surface for the square
        self.image.fill((255, 255, 255))                           # Filling in the square white
        self.rect = self.image.get_rect()                          # Getting area occupied by square
        self.rect.center = self.x, self.y                          # Setting (x,y) coordinates as center
        self.number = str(self.number)                             # Converting number into string
        self.text = font.render(self.number, 1, (0, 0, 0))         # Rendering number onto square's surface
        text_rect = self.text.get_rect(center=(80 // 2, 80 // 2))  # Getting rectangle of rendered text
        self.image.blit(self.text, text_rect)                      # Blitting text onto square's surface

def hide_cards():
    cover = pygame.Surface((80, 80)) 
    for sprite in square_group:
        cover.fill((255, 255, 255))
        sprite.image.blit(cover, (0, 0))

def reset_coord():
    global coord, original_coord
    coord = original_coord[:]

def memory(sprite):
    global num_list, level, timer_on, max_timer, cards_visible, incorrect_guesses, level_start_time, game_data, difficulty
    x, y = pygame.mouse.get_pos()
    if sprite.rect.collidepoint(x, y):
        num_list.append(sprite.number)
        sprite.rect = pygame.Rect(-80, -80, 80, 80)

        if sprite.number != str(len(num_list)):
            end_time = pygame.time.get_ticks()
            time_spent = (end_time - level_start_time) / 1000.0  # Calculate time spent in seconds
            game_data.append([level, "incorrect", time_spent])
            reset_coord()
            incorrect_guesses += 1
            num_list = []
            timer_on = 1
            cards_visible = 1
            square_group.update()
            screen.fill((255, 0, 0))  # Filling screen with red
            pygame.display.flip()  # Updating display
            pygame.time.wait(500)  # Extending green screen for 1000 milliseconds
            game_data.append([level, "incorrect", time_spent])  # Save failed level data
            level_start_time = pygame.time.get_ticks()  # Reset start time for the next attempt
            return

    if len(num_list) == len(square_group):
        win = num_list == [str(squares.number) for squares in square_group]
        end_time = pygame.time.get_ticks()
        time_spent = (end_time - level_start_time) / 1000.0  # Calculate time spent in seconds
        if win:
            level += 1
            reset_coord()
            num_list = []
            for i in range(difficulty):
                square_group.add(Square(len(square_group) + 1, make_square=False))
            timer_on = 1
            max_timer += 10
            cards_visible = 1
            screen.fill((0, 255, 0))  # Filling screen with green
            pygame.display.flip()  # Updating display
            pygame.time.wait(500)  # Extending green screen for 1000 milliseconds
            game_data.append([level-1, "correct", time_spent])  # Save completed level data
        else:
            reset_coord()
            incorrect_guesses += 1
            num_list = []
            timer_on = 1
            cards_visible = 1
            screen.fill((255, 0, 0))  # Filling screen with red
            pygame.display.flip()  # Updating display
            pygame.time.wait(500)  # Extending green screen for 1000 milliseconds
            game_data.append([level, "incorrect", time_spent])  # Save failed level data

        level_start_time = pygame.time.get_ticks()  # Reset start time for next level/attempt
        square_group.update()

def squares_init():
    for i in range(1, 4):
        square_group.add(Square(i))

counter = 0
#timer_on = 1
max_timer = 200
cards_visible = 1
level_start_time = 0  # Initialize level start time
game_data = []  # This will hold the game data for the current session

def save_game_data(game_data):
    headers = ["Level", "Result", "Time Spent (s)"]
    flattened_data = [item for sublist in game_data for item in sublist]  # Flatten the list
    is_empty = not os.path.exists("game_data.csv") or os.path.getsize("game_data.csv") == 0

    try:
        with open("game_data.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if is_empty:
                writer.writerow(headers * (len(flattened_data) // len(headers)))  # Adjust headers based on attempt count
            writer.writerow(flattened_data)
    except Exception as e:
        print(f"Error saving game data: {e}")

# def save_game_data(game_data):
#     headers = ["Level", "Result", "Time Spent (s)"]
#     flattened_data = [item for sublist in game_data for item in sublist]  # Flatten the list
#     is_empty = not os.path.exists("/Users/nguye/PIC16B-Group-Project/game_data.csv") or os.path.getsize("/Users/nguye/PIC16B-Group-Project/game_data.csv") == 0

#     with open("/Users/nguye/PIC16B-Group-Project/game_data.csv", "a", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#         if is_empty:
#             writer.writerow(headers * (len(flattened_data) // len(headers)))  # Adjust headers based on attempt count
#         writer.writerow(flattened_data)

async def main():
    global timer_on, counter, max_timer, cards_visible, level_start_time, game_data
    
    game_init()
    squares_init()
    clock = pygame.time.Clock()
    level_start_time = pygame.time.get_ticks()  # Starting timer for each level

    running = True
    #timer_on = timer_chosen 
    
    while running:
        if incorrect_guesses >= 3:
            hide_cards()
            screen.fill((255, 255, 255))
            text = font.render("GAME OVER!", 1, (0, 0, 0))
            text_rect = text.get_rect(center=(screen.get_width()//2, screen.get_height()//2)) # Centering text
            screen.blit(text, text_rect)  # Blitting text onto screen
            pygame.display.update() # Updating display to show text
            await asyncio.sleep(2)
            running = False
            continue
              
        screen.fill((0, 0, 255)) # Setting background blue
        text = font.render("Level: " + str(level), 1, (255, 255, 255)) # Displaying level 
        screen.blit(text, (0, 0)) # Blitting text at specific position
        
        if timer_chosen == 1 and timer_on == 1:
            text = font.render(" Time: " + str(max_timer - counter), 1, (255, 255, 255)) # Displaying timer
            screen.blit(text, (200, 0)) # Blitting text at specific position
            counter += 1
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for squares in square_group:
                    if squares.rect.collidepoint(event.pos):
                        hide_cards()
                        cards_visible = 0
                        timer_on = 0
                        counter = 0
                        memory(squares)

        square_group.draw(screen)

        if counter >= max_timer and timer_chosen==1:
            hide_cards()
            counter = 0
            timer_on = False
        pygame.display.update()
        clock.tick(20)
        await asyncio.sleep(0) 
        
    save_game_data(game_data)
    pygame.quit()
    
asyncio.run(main())


