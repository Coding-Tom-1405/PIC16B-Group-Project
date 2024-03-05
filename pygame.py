import pygame
import random
from glob import glob
import os

# all the possible positions for the numbers
pos = [(x, y) for x in range(1, 8) for y in range(1, 8)] 
# print(pos)
# print(pos.pop(pos.index(random.choice(pos))))
# print(pos)

def game_init():
    global screen, font

    pygame.init()
    size = w, h = 800, 800
    screen = pygame.display.set_mode((size))
    pygame.display.set_caption("Chimp Test")
    font = pygame.font.SysFont("Times New Roman", 35)
    color = (255, 0, 0)
 
    # Changing surface color
    screen.fill(color)
    pygame.display.flip()


class Square(pygame.sprite.Sprite):
    def __init__(self, number):
        super(Square, self).__init__()
        self.number = number
        self.make_image()

    def make_image(self):
        global font

        self.x, self.y = self.random_pos()
        self.image = pygame.Surface((80, 80))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.number = str(self.number)
        self.text = font.render(self.number, 1, (0, 0, 0))
        text_rect = self.text.get_rect(center=(80 // 2, 80 // 2))
        self.image.blit(self.text, text_rect)

    def update(self):
        self.make_image()
        screen.blit(self.image, (self.x, self.y))

    def random_pos(self):
        position = random.choice(pos)
        x, y = position
        pos.pop(pos.index(position))
        # x = random.randrange(0, 16)
        # y = random.randrange(0, 16)
        x = x * 80
        y = y * 80

        return x, y



g = pygame.sprite.Group()
num_order = []
level = 1
# This covers the numbers...
bgd = pygame.Surface((80, 80))
# bgd.fill((255, 0, 0))


def hide_cards():
    for sprite in g:
        bgd.fill((255, 255, 255))
        sprite.image.blit(bgd, (0, 0))


def mouse_collision(sprite):
    global num_order, level, counter_on, max_count, cards_visible

    # Check the collision only when conter is off
    x, y = pygame.mouse.get_pos()
    if sprite.rect.collidepoint(x, y):
        # bgd.fill((0, 255, 0))
        # sprite.image.blit(bgd, (0, 0))
        num_order.append(sprite.number)
        sprite.rect = pygame.Rect(-80, -80, 80, 80)

        # Check if you are wrong as you type
        if sprite.number != str(len(num_order)):
            num_order = []
            counter_on = 1
            # pygame.mouse.set_visible(False)
            g.update()
            bgd.fill((255, 0, 0))
            screen.fill((255, 0, 0))  # Fill the screen with red color
            pygame.display.flip()  # Update the display to show the green screen
            pygame.time.wait(500)  # Wait for 200 milliseconds
            screen.fill((0, 0, 0))  # Fill the screen with black color again
            pygame.display.flip()  # Update the display to show the black screen

    if len(num_order) == len(g):
        print("fine")
        print(num_order)
        # =========================== YOU GUESSED ========== 
        win = num_order == [str(s.number) for s in g]
        if win:
            level += 1
            print(str(level))
            num_order = []
            g.add(Square(len(g) + 1))
            counter_on = 1
            max_count = max_count + 10
            cards_visible = 1
            bgd.fill((255,0,0))
            screen.fill((0, 255, 0))  # Fill the screen with green color
            pygame.display.flip()  # Update the display to show the green screen
            pygame.time.wait(500)  # Wait for 200 milliseconds
            screen.fill((0, 0, 0))  # Fill the screen with black color again
            pygame.display.flip()  # Update the display to show the black screen
        else:
            num_order = []
            counter_on = 1
            cards_visible = 1
            # pygame.mouse.set_visible(False)
            bgd.fill((255,0,0))
        g.update()
        screen.fill((0,0,0))
        
def squares_init():
    for i in range(1, 4):
        g.add(Square(i))

counter = 0
counter_on = 1
max_count = 100
cards_visible = 1

def get_maxscore() -> int:
    filename = "maxscore.txt"
    if filename in os.listdir():
        with open(filename, "r") as file:
            val = file.read()
            if val == "":
                maxscore = 0
            else:
                maxscore = int(val)
    else:
        maxscore = 0
    return maxscore

def set_score(maxscore) -> None:

    with open("maxscore.txt", "w") as file:
        file.write(str(maxscore))
maxscore = get_maxscore()

def main():
    global counter_on, counter, max_count, cards_visible

    game_init()
    squares_init()
    clock = pygame.time.Clock()
    loop = 1
    # pygame.mouse.set_visible(False)
#     soundtrack("sounds/soave.ogg")
    while loop:
        screen.fill((0, 0, 0))
        text = font.render("Level: " + str(level), 1, (255, 255, 255))
        screen.blit(text, (0, 0))
        if counter_on:
            text = font.render(" Time: " + str(max_count - counter), 1, (255, 255, 255))
            screen.blit(text, (200, 0))
            counter += 1
        for event in pygame.event.get():
            # ========================================= QUIT
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    loop = 0
                    screen.fill((0,0,0))
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Click mouse and stop the timer and hide the cards
                for s in g:
                    if s.rect.collidepoint(event.pos):
                        hide_cards()
                        cards_visible = 0
                        counter_on = 0
                        counter = 0
                        mouse_collision(s)    


        g.draw(screen)
        # Hides the number...
        if counter == max_count:
            hide_cards()
            counter = 0
            counter_on = 0

                # pygame.mouse.set_visible(True)
        pygame.display.update()
        clock.tick(20)

    pygame.quit()


main()
