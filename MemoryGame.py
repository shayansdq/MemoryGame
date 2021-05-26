# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pygame, sys, random
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT= 480
REVEALSPEED = 8
BOXSIZE = 40  
GAPSIZE = 10
BOARDWIDTH = 10
BOARDHEIGHT = 7

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

assert (BOARDHEIGHT * BOARDWIDTH) % 2 == 0, 'Boards need to have an even number of Boxes for pairs of matches'

#COLORS
GRAY = (100,100,100)
NAVYBLUE = (60,60,100)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
ORANGE = (255,128,0)
PURPLE = (255,0,255)
CYAN = (0,255,255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, 'Board is too small for the number of the shapescolors defined'

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Memory Game')

    mousex = 0
    mousey = 0
    first_selection = None

    main_board = get_randomize_board()
    revealed_boxes = generate_revealed_boxes_data(False)
    DISPLAYSURF.fill(BGCOLOR)
    start_game_animation(main_board)



    while True:
        mouse_clicked = False
        DISPLAYSURF.fill(BGCOLOR)
        draw_board(main_board, revealed_boxes)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouse_clicked = True


        boxx, boxy = get_box_at_pixel(mousex, mousey)

        if boxy != None and boxy != None:
            if not revealed_boxes[boxx][boxy]:
                draw_highlight_box(boxx, boxy)
            if not revealed_boxes[boxx][boxy] and mouse_clicked:
                reveal_boxes_animation(main_board, [(boxx, boxy)])
                revealed_boxes[boxx][boxy] = True
                if first_selection == None:
                    first_selection = (boxx, boxy)
                else:
                    icon1shape, icon1color = get_shape_and_color(main_board, first_selection[0],first_selection[1])
                    icon2shape, icon2color = get_shape_and_color(main_board, boxx, boxy)
                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000)
                        cover_boxes_animation(main_board, [(first_selection[0], first_selection[1]), (boxx, boxy)])
                        revealed_boxes[boxx][boxy] = False
                        revealed_boxes[first_selection[0]][first_selection[1]] = False
                    elif has_won(revealed_boxes):
                        game_won_animation(main_board)
                        pygame.time.wait(2000)
                        main_board = get_randomize_board()
                        revealed_boxes = generate_revealed_boxes_data(False)
                        draw_board(main_board, revealed_boxes)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        start_game_animation(main_board)
                    first_selection = None
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def has_won(revealed_boxes):
    for i in revealed_boxes:
        if False in i:
            return False
    return True

def game_won_animation(board):
    covered_boxes = generate_revealed_boxes_data(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR
    for i in range(13):
        color1, color2 = color2, color1
        DISPLAYSURF.fill(color1)
        draw_board(board, covered_boxes)
        pygame.display.update()
        pygame.time.wait(300)

def get_box_at_pixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = left_top_coords_of_box(boxx, boxy)
            box_rect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if box_rect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)
def draw_highlight_box(boxx, boxy):
    left, top = left_top_coords_of_box(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10),4)
def get_randomize_board():
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color))
    random.shuffle(icons)
    num_icon_used = int(BOARDWIDTH * BOARDHEIGHT / 2)
    icons = icons[:num_icon_used] * 2
    random.shuffle(icons)

    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board
def generate_revealed_boxes_data(val):
    revealed_boxes = []
    for i in range(BOARDWIDTH):
        revealed_boxes.append([val] * BOARDWIDTH)
    return revealed_boxes

def draw_board(board, revealed):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = left_top_coords_of_box(boxx, boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                shape, color = get_shape_and_color(board, boxx, boxy)
                draw_icon(shape, color, boxx, boxy)
def left_top_coords_of_box(boxx,boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return  (left, top)
def get_shape_and_color(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]

def draw_icon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)
    left, top = left_top_coords_of_box(boxx, boxy)
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left,top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))
def start_game_animation(board):
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x, y))
    random.shuffle(boxes)
    box_groups = split_into_groups_of(8, boxes)
    covered_boxes = generate_revealed_boxes_data(False)
    draw_board(board, covered_boxes)

    for boxgroup in box_groups:
        reveal_boxes_animation(board, boxgroup)
        cover_boxes_animation(board, boxgroup)

def split_into_groups_of(group_size, the_list):
    result = []
    for i in range(0, len(the_list), group_size):
        result.append(the_list[i:i + group_size])
    return result

def reveal_boxes_animation(board, boxes_to_reveal):
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        draw_box_covers(board, boxes_to_reveal, coverage)
def cover_boxes_animation(board, boxes_to_cover):
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        draw_box_covers(board, boxes_to_cover, coverage)
def draw_box_covers(board, boxes, coverage):
    for box in boxes:
        left, top = left_top_coords_of_box(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = get_shape_and_color(board, box[0], box[1])
        draw_icon(shape, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
