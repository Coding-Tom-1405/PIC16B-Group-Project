import pygame
import random
import os
import csv
import asyncio

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
    screen.fill((0, 0, 255))

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
        global coord

        if not coord:
            coord.extend(original_coord)
        coordinates = random.choice(coord)
        coord.remove(coordinates)
        x, y = coordinates
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
bgd = pygame.Surface((80, 80))  # This covers the numbers...

#difficulty_file = "/Users/gimdong-gyu/Desktop/newProject16B/game_setting.csv" 
difficulty_file = "game_setting.csv"

with open(difficulty_file, 'r') as file:
    last_line = file.readlines()[-1]
    difficulty = int(last_line.split(',')[0])
    if last_line.split(',')[1] == 'timer\n' :
        timer_on = 1
    else :
        timer_on = 0

def hide_cards():
    for sprite in square_group:
        bgd.fill((255, 255, 255))
        sprite.image.blit(bgd, (0, 0))

def reset_coord():
    global coord, original_coord
    coord = original_coord[:]

def memory(sprite):
    global num_list, level, timer_on, max_timer, cards_visible, incorrect_guesses, loop, level_start_time, game_data

    x, y = pygame.mouse.get_pos()
    if sprite.rect.collidepoint(x, y):
        num_list.append(sprite.number)
        sprite.rect = pygame.Rect(-80, -80, 80, 80)

        if sprite.number != str(len(num_list)):
            end_time = pygame.time.get_ticks()
            time_spent = (end_time - level_start_time) / 1000.0  # Calculate time spent in seconds
            game_data.append([level, "incorrect", time_spent])

            print(str(level))
            print("incorrect")
            reset_coord()
            incorrect_guesses += 1
            num_list = []
            square_group.update()
            screen.fill((255, 0, 0))
            pygame.display.flip()
            pygame.time.wait(500)
            if incorrect_guesses >= 3:
                screen.fill((255, 255, 255))
                hide_cards()
                text = font.render("GAME OVER!", 1, (0, 0, 0))
                screen.blit(text, (400, 400))
                save_game_data(game_data) 
                loop = 0
                
            level_start_time = pygame.time.get_ticks()  # Reset start time for the next attempt
            return
        

    if len(num_list) == len(square_group):
        win = num_list == [str(squares.number) for squares in square_group]
        end_time = pygame.time.get_ticks()
        time_spent = (end_time - level_start_time) / 1000.0  # Calculate time spent in seconds
        if win:
            print(str(level))
            level += 1
            print("correct")
            reset_coord()

            num_list = []

            print(f"Adding squares, difficulty: {difficulty}")

            for _ in range(difficulty): 
                square_group.add(Square(len(square_group) + 1, make_image=False))

            max_timer += 10
            cards_visible = 1
            bgd.fill((255, 0, 0))
            screen.fill((0, 255, 0))
            pygame.display.flip()
            pygame.time.wait(500)
            screen.fill((0, 0, 0))
            pygame.display.flip()
            game_data.append([level-1, "correct", time_spent])  # Save completed level data
        else:
            print(str(level))
            print("incorrect")
            reset_coord()
            incorrect_guesses += 1
            if incorrect_guesses >= 3:
                screen.fill((255, 255, 255))
                hide_cards()
                text = font.render("GAME OVER!", 1, (0, 0, 0))
                screen.blit(text, (400, 400))
                save_game_data(game_data) 
                loop = 0
            num_list = []
            cards_visible = 1
            screen.fill((255, 0, 0))
            game_data.append([level, "incorrect", time_spent])  # Save failed level data

        level_start_time = pygame.time.get_ticks()  # Reset start time for next level/attempt
        square_group.update()
        print("-" * 25)
        screen.fill((0, 0, 0))

def init():
    pygame.init()
    return None

def squares_init():
    for i in range(1, 4):
        square_group.add(Square(i))

counter = 0
max_timer = 200
cards_visible = 1
level_start_time = 0  # Initialize level start time
game_data = []  # This will hold the game data for the current session

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
            file.write(str(level))

def save_game_data(game_data):
    headers = ["Level", "Result", "Time Spent (s)"]
    flattened_data = [item for sublist in game_data for item in sublist]  # Flatten the list
    is_empty = not os.path.exists("game_data.csv") or os.path.getsize("game_data.csv") == 0

    with open("game_data.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if is_empty:
            writer.writerow(headers * (len(flattened_data) // len(headers)))  # Adjust headers based on attempt count
        writer.writerow(flattened_data)

async def main():
    global timer_on, counter, max_timer, cards_visible, loop, level_start_time, game_data

    game_init()
    squares_init()
    clock = pygame.time.Clock()

    loop = 1
    level_start_time = pygame.time.get_ticks()  # Start timing the level

    while loop:
        screen.fill((0, 0, 255))
        text = font.render("Level: " + str(level), 1, (255, 255, 255))
        screen.blit(text, (0, 0))
        if timer_on:
            text = font.render(" Time: " + str(max_timer - counter), 1, (255, 255, 255))
            screen.blit(text, (200, 0))
            counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    loop = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                for squares in square_group:
                    if squares.rect.collidepoint(event.pos):
                        hide_cards()
                        cards_visible = 0
                        timer_on = 0
                        counter = 0
                        memory(squares)

        square_group.draw(screen)

        if counter >= max_timer:
            #hide_cards()
            counter = 0
        pygame.display.update()
        clock.tick(20)
        await asyncio.sleep(0)
    pygame.quit()

asyncio.run(main())
update_maxlevel(level)


