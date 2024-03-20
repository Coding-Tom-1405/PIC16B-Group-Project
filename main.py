# Import necessary packages
import pygame
import random
import os
import csv

# Creating coordinate grid for squares
coord_grid = [(x, y) for x in range(1, 10) for y in range(1, 10)]
original_coord = coord_grid[:]                              # Replica to update coord after each level

# Creating the group of square and numbers
square_group = pygame.sprite.Group()                        # Grouping of the squares
num_list = []                                               # List to append the square's numbers

# Creating game settings
level = 1                                                   # Initial level value
incorrect_guesses = 0                                       # Initial incorrect guesses made
difficulty = 1                                              # Default difficulty mode user chose

# Time setting
time_passed = 0                                             # Stopwatch
timer_on_or_off = 1                                         # Boolean indicating if timer is on
timer = 100                                                 # Initial timer for lvl 1
start_time = 0                                              # Initial level start time

# Storage for data visualization
game_data = []

# Taking into account user's difficulty and/or challenge chosen
difficulty_file = "game_setting.csv"                        
with open(difficulty_file, 'r') as file:                    # Accessing game_setting.csv
    last_line = file.readlines()[-1]                        # Accessing the last entry row
    difficulty = int(last_line.split(',')[0])               # Splitting last line with comma delimiters
                                                            # Taking the 1st integer variable as difficulty
    if last_line.split(',')[1] == 'timer\n' :               # Checking if 2nd element says timer chosen
        timer_chosen = 1
    else :                                                  # Checking if 2nd element says timer NOT chosen
        timer_chosen = 0

def game_init():
    """
    Initializing game
    """
    global font, screen
    pygame.init()                                             # Initializing pygame modules
    screen = pygame.display.set_mode((800, 800))              # Setting screen size
    pygame.display.set_caption("Chimp Test")                  # Setting game name
    font = pygame.font.SysFont("Times New Roman", 40)         # Setting general text font and size
    screen.fill((0, 0, 255))                                  # Setting background blue

class Square(pygame.sprite.Sprite): 
    """
    Class representing Square object in the game
    """
    def __init__(self, number, make_square=True):
        """
        Initializing Square object with given number

        Args:
            number (int): Number associated with square
            make_square (bool): Flag indicating whether to create the squares

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
        global coord_grid
        if not coord_grid:                                 # Checking if coord grid is empty
            coord_grid.extend(original_coord)              # Refilling the list
        coordinates = random.choice(coord_grid)            # Choosing random coordinates
        coord_grid.remove(coordinates)                     # Removing the chosen coordinates to prevent repeats
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

def squares_init():
    """
    Initializes the first batch of squares (for Level 1)
    """
    for i in range(1, 4):                     # Iterating over range 1 to 3 (creating three squares)
        square_group.add(Square(i))           # Adding Square objects with its number to square_group
        
def hide_square():
    """
    Hides the square's numbers by covering them with a white surface
    """
    cover = pygame.Surface((80, 80))           # Creating a 80 x 80 white surface 
    for sprite in square_group:                # Iterating through each square in square_group
        cover.fill((255, 255, 255))            # Filling the surface with white
        sprite.image.blit(cover, (0, 0))       # Blitting the white surface onto the squares

def reset_coord():
    """
    Resets the coordinate grid so the squares can take any of the 81 positions after a new level
    """
    global coord_grid, original_coord       # Accessing the global variables
    coord_grid = original_coord[:]          # Resetting coord to original_coord by creating a shallow copy

def memory(sprite):
    """
    Memory recall game logic
    
    Args:
        sprite (Square): Square object that was clicked

    Returns:
        None
    """
    global num_list, level, timer_on_or_off, timer, incorrect_guesses, start_time, game_data, difficulty

    x, y = pygame.mouse.get_pos()                      # Getting current mouse position 
    if sprite.rect.collidepoint(x, y):                 # Checking if mouse is within the square's boundary
        num_list.append(sprite.number)                 # Appending square's number to num_list
        sprite.rect = pygame.Rect(-80, -80, 80, 80)    # Moving square off the screen

        #Wrong Square Clicked Situation
        if sprite.number != str(len(num_list)):    
            end_time = pygame.time.get_ticks()     # Ending pygame clock
            time_spent = (end_time - start_time) / 1000.0  # Calculating time spent in seconds  
            incorrect_guesses += 1                 # Increasing amount of incorrect guesses by 1
            print("Incorrect! Lives: ", 3 - incorrect_guesses) # Printing checkpoint message
            reset_coord()                          # Resetting coordinate grid
            num_list = []                          # Emptying num_list for new round
            timer_on_or_off = 1                    # Setting timer back on
            square_group.update()                  # Updating square group
            screen.fill((255, 0, 0))               # Displaying red screen
            pygame.display.flip()                  # Updating display screen
            pygame.time.wait(500)                  # Extending red screen for 500 milliseconds
            game_data.append([level, 
                              "incorrect", 
                              time_spent])         # Append round results to game_data
            return

    if len(num_list) == len(square_group):        # Checking if all squares were clicked
        win = num_list == [str(squares.number) for squares in square_group] # Setting win condition
        end_time = pygame.time.get_ticks()    # Getting end_time of level
        time_spent = (end_time - start_time) / 1000.0  # Calculating level time spent in seconds

        # Win Situation
        if win:
            print("Correct! You Passed Level ", level)
            print("--------------------------------")
            reset_coord()                         
            num_list = []
            for i in range(difficulty):           # Adding number of squares equal to difficulty chosen
                square_group.add(Square(len(square_group) + 1, make_square=False)) 
            timer_on_or_off = 1            
            timer += 10                       # Increasing timer for next level
            screen.fill((0, 255, 0))              # Displaying green screen
            pygame.display.flip()                 # Updating display screen
            pygame.time.wait(500)                 # Extending green screen for 1000 milliseconds
            game_data.append([level, 
                              "correct", 
                              time_spent])        # Append round results to game_data  
            level += 1                            # Increasing level by 1
         

        # Win Not Met Situation
        else:
            incorrect_guesses += 1
            print("Incorrect! Lives: ", 3 - incorrect_guesses)
            reset_coord()                         
            num_list = []
            timer_on_or_off = 1
            screen.fill((255, 0, 0))              # Filling screen with red
            pygame.display.flip()  
            pygame.time.wait(500)
            game_data.append([level, 
                              "incorrect", 
                              time_spent])        # Append round results to game_data            

        start_time = pygame.time.get_ticks()      # Resetting start time for next level/attempt
        square_group.update()                     # Updating square group


def save_game_data(game_data):
    """
    Saving the game data results into a CSV file

    Args:
        game data(list of lists): The list of data to be saved, each sublist represents the results of a round

    Results:
        None
    """
    headers = ["Level", "Result", "Time Spent"]                       # Defining headers for CSV file
    flattened_data = [item for sublist in game_data for item in sublist]  # Flattening the list

    # Checking if CSV file is empty or doesn't exist
    is_empty = not os.path.exists("game_data.csv") or os.path.getsize("game_data.csv") == 0 
    
    try:
        with open("game_data.csv", "a", newline="") as csvfile:                   # Opening CSV file in append mode
            writer = csv.writer(csvfile)
            if is_empty:                                                          # Writing header if empty
                writer.writerow(headers * (len(flattened_data) // len(headers)))  # adjustting for multiple tries
            writer.writerow(flattened_data)
            
    except Exception as e:                                                        # Handling exceptions
        print(f"Error saving game data: {e}")

def main():
    """
    Main function for running the game, including initializing the game settings, 
    managing the game loop, and updating game state and display
    """

    # Accessing global variables
    global timer_on_or_off, counter, timer, start_time, time_passed, game_data
    
    game_init()                                               # Initializing the game (pygame.init() in here)
    squares_init()                                            # Initializing lvl 1 squares
    clock = pygame.time.Clock()                               # Getting clock to time user's levels
    start_time = pygame.time.get_ticks()                      # Starting timer for each level

    running = True                                            # Establishing initial boolean for loop running

    # Initial Welcome Message
    print("WELCOME TO THE CHIMP TEST GAME! HAVE FUN!")
    print("-----------------------------------------")
    
    while running:
        # Ending Situation
        if incorrect_guesses >= 3:              
            # Ending Message
            print("--------------------------------")
            print("GAME OVER! Your Score: ", level)           
            
            hide_square()                                     # Hiding cards in end screen 
            screen.fill((255, 255, 255))                      # Filling background with white
            text = font.render("GAME OVER!", 1, (0, 0, 0))    # Rendering black "GAME OVER!" text
            text_rect = text.get_rect(center=(screen.get_width()//2, screen.get_height()//2)) # Centering text
            screen.blit(text, text_rect)                      # Blitting text onto screen
            pygame.display.update()                           # Updating display to show text
            
            save_game_data(game_data)                         # Saving game data
            running = False                                   # Setting game loop boolean to false
            continue                                          # Skipping rest of loop
              
        screen.fill((0, 0, 255))                              # Setting background blue
        text = font.render("Level: " + str(level), 1, (255, 255, 255)) # Displaying level text
        screen.blit(text, (0, 0))                             # Blitting text at specific position

        # User Chose Timer Mode Situation
        if timer_on_or_off == 1 and timer_chosen == 1:        
            text = font.render(" Time: " + str(timer - time_passed), 1, (255, 255, 255)) # Displaying timer
            screen.blit(text, (200, 0))                       
            time_passed += 1                                  # Incrementing stopwatch
            
        for event in pygame.event.get():                      
            if event.type == pygame.QUIT:                     # Checking if user manually quits
                running = False        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:  # Checking if user clicks keys
                running = False                         
            if event.type == pygame.MOUSEBUTTONDOWN:          # Checking if clicked mouse
                for squares in square_group:           
                    # Mouse Clicks Square Situation
                    if squares.rect.collidepoint(event.pos):   
                        hide_square()                         # Hiding cards
                        timer_on_or_off = 0                   # Turning timer off
                        time_passed = 0                       # Resetting stopwatch
                        memory(squares)                       # Activating memory logic with clicked square

        square_group.draw(screen)                             # Drawing the remaining squares on screen

        # Time-is-up Situation
        if time_passed >= timer and timer_chosen == 1:        
            hide_square()                                      
            time_passed = 0
            timer_on_or_off = 0
            
        pygame.display.update()                               
        clock.tick(20)                                        # Limiting frame rate to 20 frames per second
        
    pygame.quit()
    
main()
