import pygame
from Engine import ChessEngine as Chess
from ChessUtility import indexToRF, rfToIndex
from Enums.PieceEnum import PieceEnum
from Move import Move
from Enums.SideEnum import SideEnum

import os


def get_board_index(x, y):
    column = x // pixel_size
    row = y // pixel_size
    return column + 8 * row

def draw_square(size, board_index):
    currentRow = board_index // 8 * pixel_size
    currentColumn = board_index % 8 * pixel_size
    return pygame.Rect(currentColumn, currentRow, size, size)


def draw_board(canvas, board):
    canvas.fill((255, 255, 255))
    squares: list[pygame.Rect]= []
    # Draw squares
    for i in range(64):
        currentRow = i // 8

        odd = (i + currentRow) % 2
        color = (255, 255, 255) if odd else (220, 220, 220)
        ays = pygame.draw.rect(canvas, color, draw_square(pixel_size, i))
        squares.append(ays)

    for i, square in enumerate(squares):
        if board[i] is None:
            continue
        canvas.blit(
            pygame.PIECE_IMAGES[str(board[i])], square
        )


def player_vs_computer(canvas):
    exit = False
    instance = Chess()
    start_pressed_board_position = 0
    draw_board(canvas, instance.board)
    while not exit:
        for event in pygame.event.get():
            if instance.SideToPlay is SideEnum.BLACK:
                move = instance.search_moves()
                instance.makeMove(move)
                draw_board(canvas, instance.board)
                pygame.draw.rect(canvas, (255, 0, 0), draw_square(
                    pixel_size, move.startPosition), 5)
                pygame.draw.rect(canvas, (255, 0, 0), draw_square(
                    pixel_size, move.endPosition), 5)
                pygame.mixer.music.play()
            current_mouse_location = pygame.mouse.get_pos()
            if event.type is pygame.QUIT:
                exit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_pressed_board_position = get_board_index(
                    current_mouse_location[0], current_mouse_location[1]
                )
                all_moves = instance.generate_legal_moves()
                for moves in all_moves:
                    if moves.startPosition is start_pressed_board_position:
                        pygame.draw.rect(canvas, (0, 255, 0), draw_square(
                            pixel_size, moves.endPosition), 5)
            if event.type == pygame.MOUSEBUTTONUP:
                draw_board(canvas, instance.board)
                current_board_position = get_board_index(
                    current_mouse_location[0], current_mouse_location[1]
                )
                toMake = f"{indexToRF(start_pressed_board_position)}{indexToRF(current_board_position)}"
                all_moves = instance.generate_legal_moves()
                rf_moves = []
                total = 0
                for move in all_moves:
                    total += 1
                    rf_moves.append(
                        f"{move.startRf}{move.endRf}"
                    )
                if toMake not in rf_moves:
                    continue
                instance.makeMove(all_moves[rf_moves.index(toMake)])
                draw_board(canvas, instance.board)
                pygame.mixer.music.play()
        if instance.checkmated:
            exit = True
        pygame.display.update()

def player_vs_player(canvas):
    exit = False
    instance = Chess()
    start_pressed_board_position = 0
    draw_board(canvas, instance.board)
    while not exit:
        for event in pygame.event.get():
            current_mouse_location = pygame.mouse.get_pos()
            if event.type is pygame.QUIT:
                exit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_pressed_board_position = get_board_index(
                    current_mouse_location[0], current_mouse_location[1]
                )
                all_moves = instance.generate_legal_moves()
                for moves in all_moves:
                    if moves.startPosition is start_pressed_board_position:
                        pygame.draw.rect(canvas, (0, 255, 0), draw_square(
                            pixel_size, moves.endPosition), 5)
            if event.type == pygame.MOUSEBUTTONUP:
                draw_board(canvas, instance.board)
                current_board_position = get_board_index(
                    current_mouse_location[0], current_mouse_location[1]
                )
                toMake = f"{indexToRF(start_pressed_board_position)}{indexToRF(current_board_position)}"
                all_moves = instance.generate_legal_moves()
                rf_moves = []
                total = 0
                for move in all_moves:
                    total += 1
                    rf_moves.append(
                        f"{move.startRf}{move.endRf}"
                    )
                if toMake not in rf_moves:
                    continue
                instance.makeMove(all_moves[rf_moves.index(toMake)])
                draw_board(canvas, instance.board)
                pygame.mixer.music.play()
        if instance.checkmated:
            exit = True
        pygame.display.update()

def practice_mode(canvas):
    exit = False
    instance = Chess()
    start_pressed_board_position = -1
    draw_board(canvas, instance.board)
    while not exit:
        for event in pygame.event.get():
            current_mouse_location = pygame.mouse.get_pos()
            if event.type is pygame.QUIT:
                exit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_pressed_board_position = get_board_index(
                    current_mouse_location[0], current_mouse_location[1]
                )
            if event.type == pygame.MOUSEBUTTONUP:
                draw_board(canvas, instance.board)
                current_board_position = get_board_index(
                    current_mouse_location[0], current_mouse_location[1]
                )
                if start_pressed_board_position == -1 or instance.board[start_pressed_board_position] is None:
                    continue
                instance.makeMove(Move(start_pressed_board_position, current_board_position, instance.board[start_pressed_board_position], instance.board[current_board_position]))
                draw_board(canvas, instance.board)
                pygame.mixer.music.play()
        if instance.checkmated:
            exit = True
        pygame.display.update()

def load_images(store):
    images = os.listdir("piece_images/")
    for image in images:
        loaded_image = pygame.image.load(os.path.join("piece_images", image))
        refined_image = pygame.transform.scale(
            loaded_image, (canvas_size//8, canvas_size//8))
        store[image[0:2]] = refined_image

def draw_menu(canvas):
    running = True
    while running:
        canvas.fill((255,255,255))
        pvp_square = pygame.draw.rect(canvas, (0, 0, 0), draw_square(
            pixel_size, 19), 2)
        pvai_square = pygame.draw.rect(canvas, (0, 0, 0), draw_square(
            pixel_size, 20), 2)
        practice_square = pygame.draw.rect(canvas, (0, 0, 0), draw_square(
            pixel_size, 21), 2)
        quit_square = pygame.draw.rect(canvas, (0, 0, 0), draw_square(
            pixel_size, 22), 2)
        canvas.blit(pygame.TEXT_FONT.render("PvP", True, (0, 0, 0)),
                    (pvp_square.left, pvp_square.top))
        canvas.blit(pygame.TEXT_FONT.render("PvAI", True, (0, 0, 0)),
                    (pvai_square.left, pvai_square.top))
        canvas.blit(pygame.TEXT_FONT.render("Practice", True, (0, 0, 0)),
                    (practice_square.left, practice_square.top))
        canvas.blit(pygame.TEXT_FONT.render("Quit", True, (0, 0, 0)),
                    (quit_square.left, quit_square.top))
        for event in pygame.event.get():
            current_mouse_location = pygame.mouse.get_pos()
            if event.type == pygame.QUIT: 
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                start_pressed_board_position = get_board_index(
                    current_mouse_location[0], current_mouse_location[1]
                )
                print(start_pressed_board_position)
                if start_pressed_board_position == 19:
                    player_vs_player(canvas)
                elif start_pressed_board_position == 20:
                    player_vs_computer(canvas)
                elif start_pressed_board_position == 21:
                    practice_mode(canvas)
                elif start_pressed_board_position == 22:
                    running=False
        pygame.display.update()

if __name__ == "__main__":
    
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.mixer.music.load("move.mp3")
    pygame.TEXT_FONT = pygame.font.SysFont('Arial', 20)
    pygame.PIECE_IMAGES = {}

    canvas_size = 512
    pixel_size = canvas_size // 8
    canvas = pygame.display.set_mode((canvas_size, canvas_size))
    load_images(pygame.PIECE_IMAGES)
    print(pygame.PIECE_IMAGES)

    pygame.display.set_caption("CHESS")
    draw_menu(canvas)


