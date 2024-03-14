import pyglet
from pyglet.gl import glClearColor
import random
import time
import os
import csv

# all the possible positions for the numbers
coord = [(x, y) for x in range(1, 10) for y in range(1, 10)] 
original_coord = coord[:]

def game_init():
    global window, font
    
    window = pyglet.window.Window(800, 800, caption="Chimp Memory Test")
    font = pyglet.font.load("Times New Roman", 35)
 
    # Changing surface color
    glClearColor(0, 0, 1, 1)  # Set background color to blue (R=0, G=0, B=1)
    window.clear()  # Clears the window with the specified background color

def draw_list(list):
    for l in list:
        l.draw()

class Square(pyglet.sprite.Sprite):
     
    def __init__(self, number, batch, make_image = True):
        super(Square, self).__init__(img = pyglet.image.SolidColorImagePattern(color=(255, 255, 255, 255)).create_image(80, 80), batch = batch)
        self.number = number
        square_list.append(self)
        self.make_image()

        
    def random_coord(self):
        global coord  # Access the global coord list
        if not coord:
            coord.extend(original_coord)
        coordinates = random.choice(coord)
        x, y = coordinates
        coord.remove(coordinates)  # Remove the chosen position from the list
        x = x * 80
        y = y * 80
        return x, y
    
    def make_image(self):
        self.x, self.y = self.random_coord()
        self.number = str(self.number)
        self.text = pyglet.text.Label(self.number,
                                      font_name="Times New Roman",
                                      font_size=35,
                                      color=(0, 0, 0, 255),
                                      x=self.x + 40,  # Adjusted positioning
                                      y=self.y + 40,  # Adjusted positioning
                                      anchor_x='center',
                                      anchor_y='center'
                                     )

    
    def draw(self):
        super(Square, self).draw()
        self.text.draw()


global square_list
square_list = []
square_batch = pyglet.graphics.Batch()

num_list = []
level = 1
incorrect_guesses = 0

        
def reset_coord():
    global coord, original_coord
    coord = original_coord[:]  # Reset pos to its original state        


def memory(x, y, button):
    global num_list, square_list, level, timer_on, max_timer, cards_visible, incorrect_guesses, loop
    clicked_square  = None
    # Check the collision only when conter is off
        
    for square in square_list:
        if square.x <= x < square.x + 80 and square.y <= y < square.y + 80:

            num_list.append(square.number)
            square.x = -80
            square.y = -80
            clicked_square = square
            square.opacity = 0
            for square in square_list:
                square.text = pyglet.text.Label()

            
            # Check if you are wrong as you type
            if clicked_square.number != str(len(num_list)):
                print(str(level))
                reset_coord()
                cards_visible = 1
                incorrect_guesses += 1
                print("Strikes: ", incorrect_guesses)
                num_list = []
                timer_on = 1
                square_list = []
                for i in range(1, level+3):
                    square = Square(i, batch=square_batch)
                    square.make_image()

                glClearColor(1.0, 0.0, 0.0, 1.0)  # Clear with red color
                window.clear()
                window.flip()
                time.sleep(1)
 
                
                if incorrect_guesses >= 3:
                    print("Game Over!")
                    loop = False  # Terminate the game loop
                    return

    if clicked_square is None:
            return

    if len(num_list) == len(square_list):
        win = num_list == [str(square.number) for square in square_list]
        if win:
            print(str(level))
            level += 1
            print("correct")
            reset_coord()
            cards_visible = 1
            num_list = []
            square_list = []
            for i in range(1, level+3):
                square = Square(i, batch = square_batch)
                square.make_image()  # Call make_image for each new square
            timer_on = 1
            max_timer += 10
            cards_visible = 1
            glClearColor(0.0, 1.0, 0.0, 1.0)  # Clear with green color
            window.clear()
            window.flip()
            time.sleep(1)

            
        else:
            print(str(level))
            reset_coord()
            cards_visible = 1
            incorrect_guesses += 1
            print("Strikes: ", incorrect_guesses)
            if incorrect_guesses >= 3:
                print("Game Over!")
                loop = False  # Terminate the game loop
                return
            num_list = []
            timer_on = 1
            
            square_list = []
            for i in range(1, level+3):
                square = Square(i, batch=square_batch)
                square.make_image()
            glClearColor(1.0, 0.0, 0.0, 1.0)  # Clear with red color
            window.clear()
            window.flip()
            time.sleep(1)
            window.clear()
            window.flip()
           
        square_batch.draw()
        print("-"*25)        

def clear_window(dt):
    window.clear()
    window.flip()
    
def squares_init():
    global square_batch
    for i in range(1, 4):
        square = Square(i, batch = square_batch)



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


def update_maxlevel(level):
    maxlevel = get_maxlevel()
    if level > maxlevel:
        with open("maxlevel.txt", "w") as file:
            file.write(str(maxlevel))
        
def save_game_data(game_data):
    # Check if the file is empty
    is_empty = os.path.getsize("game_data.csv") == 0

    with open("game_data.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if is_empty:  # Write the header only if the file is empty
            writer.writerow(["Level"])  # Write header
        for data in game_data:
            writer.writerow([data["level"]])


def main():
    global timer_on, counter, max_timer, cards_visible, loop, game_data

    game_init()
    squares_init()
    clock = pyglet.clock.Clock()

    loop = True
    game_data = []



    @window.event
    def on_draw():
        pyglet.gl.glClearColor(0, 0, 1, 1)  # Set clear color to blue
        window.clear()  # Clear the window with the specified background color
        level_label = pyglet.text.Label("Level: " + str(level),
                                        font_name="Times New Roman",
                                        font_size=35,
                                        x=0,
                                        y=750
                                       )

        for square in square_list:
            square.draw()
        level_label.draw()
        if timer_on:
            time_label = pyglet.text.Label(" Time: " + str(max_timer - counter),
                                           font_name="Times New Roman",
                                           font_size=35,
                                           x=200,
                                           y=750
                                          )
            time_label.draw()
          # Draw the square batch


       
    @window.event
    def on_mouse_press(x, y, button, modifiers):
        global counter, timer_on, loop
        if button == pyglet.window.mouse.LEFT:
            # Pass clicked coordinates to memory function
            memory(x, y, button)
    
    def update(dt):
        global counter, timer_on, loop
        if timer_on:
            counter += 1
            if counter >= max_timer:
                counter = 0
                timer_on = False
    pyglet.clock.schedule_interval(update, 1.0 / 60)
    
    while loop:
        pyglet.clock.tick()  # Ensures a smooth frame rate
        window.dispatch_events()  # Dispatches window events
        window.clear()  # Clears the window
        on_draw()  # Calls the draw function
        window.flip()  # Displays the updated window


    print("You Score: ", level)
    # Append current level data to game data
    game_data.append({"level": level})

    # Save game data to CSV
    save_game_data(game_data)

    update_maxlevel(level)

main()










# import pygame
# import random
# from glob import glob
# import os
# import csv

# # all the possible positions for the numbers
# coord = [(x, y) for x in range(1, 10) for y in range(1, 10)] 
# original_coord = coord[:]

# def game_init():
#     global screen, font

#     pygame.init()
#     screen = pygame.display.set_mode((800, 800))
#     pygame.display.set_caption("Chimp Memory Test")
#     font = pygame.font.SysFont("Times New Roman", 35)
 
#     # Changing surface color
#     screen.fill((0,0,255))



# class Square(pygame.sprite.Sprite):
     
#     def __init__(self, number, make_image=True):
#         super(Square, self).__init__()
#         self.number = number
#         if make_image:
#             self.make_image()
        
        
#     def update(self):
        
#         self.make_image()
#         screen.blit(self.image, (self.x, self.y))

        
#     def random_coord(self):
        
#         global coord  # Access the global pos list

#         if not coord:
#             # Regenerate pos list if it's empty
#             coord.extend(original_coord)
#         coordinates = random.choice(coord)
#         x, y = coordinates
#         coord.remove(coordinates)  # Remove the chosen position from the list
#         x = x * 80
#         y = y * 80
#         return x, y
    
#     def make_image(self):
#         global font
#         self.x, self.y = self.random_coord()
#         self.image = pygame.Surface((80, 80))
#         self.image.fill((255, 255, 255))
#         self.rect = self.image.get_rect()
#         self.rect.center = self.x, self.y
#         self.number = str(self.number)
#         self.text = font.render(self.number, 1, (0, 0, 0))
#         text_rect = self.text.get_rect(center=(80 // 2, 80 // 2))
#         self.image.blit(self.text, text_rect)

# square_group = pygame.sprite.Group()
# num_list = []
# level = 1
# incorrect_guesses = 0
# # This covers the numbers...
# bgd = pygame.Surface((80, 80))


# def hide_cards():
#     for sprite in square_group:
#         bgd.fill((255, 255, 255))
#         sprite.image.blit(bgd, (0, 0))
# def reset_coord():
#     global coord, original_coord
#     coord = original_coord[:]  # Reset pos to its original state        



# def memory(sprite):
#     global num_list, level, timer_on, max_timer, cards_visible, incorrect_guesses, loop
#     # Check the collision only when conter is off
#     x, y = pygame.mouse.get_pos() 
#     if sprite.rect.collidepoint(x, y):
#         num_list.append(sprite.number)
#         sprite.rect = pygame.Rect(-80, -80, 80, 80)

#         # Check if you are wrong as you type
#         if sprite.number != str(len(num_list)):
#             print(str(level))
#             print("incorrect")
#             reset_coord()
#             incorrect_guesses += 1
#             num_list = []
#             timer_on = 1
#             square_group.update()
#             screen.fill((255, 0, 0))  # Fill the screen with red color
#             pygame.display.flip()  # Update the display
#             pygame.time.wait(500)  # Wait for 500 milliseconds
#             if incorrect_guesses >= 3:
#                 loop = 0  # Terminate the game loop
#             return




#     if len(num_list) == len(square_group):
#         win = num_list == [str(squares.number) for squares in square_group]
#         if win:   
#             print(str(level))
#             level += 1
#             print("correct")
#             reset_coord()
            
#             num_list = []
#             square_group.add(Square(len(square_group) + 1, make_image = False))
#             timer_on = 1
#             max_timer += 10
#             cards_visible = 1
#             bgd.fill((255,0,0))
#             screen.fill((0, 255, 0))  # Fill the screen with green color
#             pygame.display.flip()  # Update the display to show the green screen
#             pygame.time.wait(500)  # Wait for 200 milliseconds
#             screen.fill((0, 0, 0))  # Fill the screen with black color again
#             pygame.display.flip()  # Update the display to show the black screen
            
            
#         else:
#             print(str(level))
#             print("incorrect")
#             reset_coord()
#             incorrect_guesses += 1
#             if incorrect_guesses >= 3:
#                 loop = 0  # Terminate the game loop
#             num_list = []
#             timer_on = 1
#             cards_visible = 1
#             screen.fill((255, 0, 0))  # Fill the screen with red color
           
#         square_group.update()
#         print("-"*25)
#         screen.fill((0, 0, 0))  # Fill the screen with black color
        


# def init():
#     pygame.init()
#     return None
    
# def squares_init():
#     for i in range(1, 4):
#         square_group.add(Square(i))

# counter = 0
# timer_on = 1
# max_timer = 200
# cards_visible = 1

# def get_maxlevel() -> int:
#     filename = "maxlevel.txt"
#     if filename in os.listdir():
#         with open(filename, "r") as file:
#             leader = file.read()
#             if leader == "":
#                 maxlevel = 0
#             else:
#                 maxlevel = int(leader)
#     else:
#         maxlevel = 0
#     return maxlevel

# def update_maxlevel(level):
#     maxlevel = get_maxlevel()
#     if level > maxlevel:
#         with open("maxlevel.txt", "w") as file:
#             file.write(str(maxlevel))

# def save_game_data(game_data):
#     # Check if the file is empty
#     is_empty = os.path.getsize("game_data.csv") == 0

#     with open("game_data.csv", "a", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#         if is_empty:  # Write the header only if the file is empty
#             writer.writerow(["Level"])  # Write header
#         for data in game_data:
#             writer.writerow([data["level"]])
            
# def main():
#     global timer_on, counter, max_timer, cards_visible, loop

#     game_init()
#     squares_init()
#     clock = pygame.time.Clock()

#     loop = 1

#     while loop:
#         screen.fill((0,0,255))
#         text = font.render("Level: " + str(level), 1, (255, 255, 255))
#         screen.blit(text, (0, 0))
#         if timer_on:
#             text = font.render(" Time: " + str(max_timer - counter), 1, (255, 255, 255))
#             screen.blit(text, (200, 0))
#             counter += 1
#         for event in pygame.event.get():
#             # ========================================= QUIT
#             if event.type == pygame.QUIT:
#                 loop = 0
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_s:
#                     loop = 0
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 # Click mouse and stop the timer and hide the cards
#                 for squares in square_group:
#                     if squares.rect.collidepoint(event.pos):
#                         hide_cards()
#                         cards_visible = 0
#                         timer_on = 0
#                         counter = 0
#                         memory(squares)    


#         square_group.draw(screen)
#         # Hides the number...
#         if counter == max_timer:
# #             hide_cards()
#             counter = 0
#             timer_on = 0


#         pygame.display.update()
#         clock.tick(20)
        
#     # Append current level data to game data
#     game_data.append({"level": level}) 

#     # Save game data to CSV
#     save_game_data(game_data)
    
#     pygame.quit()

    
# main()
# update_maxlevel(level)
