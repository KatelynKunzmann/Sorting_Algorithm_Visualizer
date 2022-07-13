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

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('arial', 20)
    LARGE_FONT = pygame.font.SysFont('arial', 25)

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


def draw(draw_info):
    draw_info.window.fill(draw_info.BG_COLOR)

    controls = draw_info.FONT.render("R - Reset | SPACEBAR - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    # Must subtract the width of the text/2 by the width of the screen/2 to land in the proper x coordinate for the text
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 5))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | M - Merge Sort | Q - Quick Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 35))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_pos = {}, clear_bg = False):
    lst = draw_info.lst

    if clear_bg:
        clear_rectangle = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BG_COLOR, clear_rectangle)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        # To determine correct height, must subtract val and min_val THEN multiply by block height
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        # Every 3 elements will have 3 different shades of gray, then it resets
        color = draw_info.GRADIENTS[i % 3]

        if i in color_pos:
            color = color_pos[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    if clear_bg:
        pygame.display.update()

def generate_start_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

######################## SORTING ALGORITHMS ###############################

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                #draw_list()
                # Yield keyword Pauses the execution sort of halfway through and stores the current state of the function - creates a generator
                # Will allow us to continue using controls like 'exit'
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True

    return lst

######################## END SORTING ALGORITHMS ###############################

def main():
    running = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_start_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algo = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None

    # Constant loop to keep window active
    while running:
        # Maximum amount of times the loop can run per second (fps)
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration: # Generator is finished
                sorting = False
        else:
            draw(draw_info)

        draw(draw_info)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_start_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_generator = sorting_algo(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False

        
    pygame.quit()


if __name__ == "__main__":
    main()