import pygame
import random
import math
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GRAY = 128, 128, 128
    BG_COLOR = WHITE

    # Side padding and top padding 
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = round((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def generate_start_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst



def main():
    running = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_start_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)

    # Constant loop to keep window active
    while running:
        # Maximum amount of times the loop can run per second (fps)
        clock.tick(60)

        pygame.display.update()

        for event in pygame.event.get():
            if event == pygame.QUIT:
                run = False
        
    pygame.quit()


if __name__ == "__main__":
    main()