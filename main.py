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

def checkmate_screen(canvas, winning_side: SideEnum):
    closed = False 
    canvas.blit(pygame.TEXT_FONT.render(f"{winning_side.name} has won. Press X to go back to main menu", True, (150, 0, 150)),
                (0, 0))
    pygame.display.update()
    while not closed:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                closed = True

def stalemate_screen(canvas):
    closed = False
    canvas.blit(pygame.TEXT_FONT.render(f"Stalemate. Press X to go back to main menu", True, (150, 0, 150)),
                (0, 0))
    pygame.display.update()
    while not closed:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                closed = True


def player_vs_computer(canvas, start_side: SideEnum, depth: int):
    exit = False
    instance = Chess()
    start_pressed_board_position = 0
    draw_board(canvas, instance.board)
    while not instance.checkmated and not instance.stalemated and not exit:
        pygame.display.update()
        for event in pygame.event.get():
            if instance.SideToPlay is (SideEnum.WHITE if start_side is SideEnum.BLACK else SideEnum.BLACK):
                moves = instance.generate_legal_moves()
                move = instance.search_moves(moves, depth)
                instance.makeMove(move)
                instance.checkmated = instance.in_checkmate()
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
        instance.checkmated = instance.in_checkmate()
        instance.stalemated = instance.in_stalemate()
        
    if instance.checkmated:
        checkmate_screen(
            canvas, SideEnum.WHITE if instance.SideToPlay is SideEnum.BLACK else SideEnum.BLACK)
    if instance.in_stalemate():
        stalemate_screen(canvas)

def player_vs_player(canvas):
    exit = False
    instance = Chess()
    start_pressed_board_position = 0
    draw_board(canvas, instance.board)
    while not exit and not instance.stalemated and not instance.checkmated:
        pygame.display.update()
        for event in pygame.event.get():
            current_mouse_location = pygame.mouse.get_pos()
            if event.type is pygame.QUIT:
                exit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[2]:
                    instance.unmakeMove()
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
        instance.checkmated = instance.in_checkmate()
        instance.stalemated = instance.in_stalemate()

    if instance.checkmated:
        checkmate_screen(
            canvas, SideEnum.WHITE if instance.SideToPlay is SideEnum.BLACK else SideEnum.BLACK)
    if instance.in_stalemate():
        stalemate_screen(canvas)

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

    # text colours
    selected_colour = (0, 150, 0)
    unselected_colour = (0, 0, 0)

    selected_difficulty = 1
    selected_play_side = SideEnum.WHITE

    # options dictionary with respective actions to be performed.
    options = {
        19: ("PvP", lambda: player_vs_player(canvas)),
        20: ("PvAI", lambda: player_vs_computer(canvas, selected_play_side, selected_difficulty)),
        21: ("Practice", lambda: practice_mode(canvas)),
        22: ("Quit", lambda: set_running(False)),
        41: ("Easy", lambda: set_selected_difficulty(1)),
        42: ("Medium", lambda: set_selected_difficulty(2)),
        43: ("Hard", lambda: set_selected_difficulty(3)),
        45: ("White", lambda: set_selected_play_side(SideEnum.WHITE)),
        46: ("Black", lambda: set_selected_play_side(SideEnum.BLACK))
    }

    def set_running(value):
        nonlocal running
        running = value

    def set_selected_difficulty(difficulty):
        nonlocal selected_difficulty
        selected_difficulty = difficulty

    def set_selected_play_side(side):
        nonlocal selected_play_side
        selected_play_side = side

    while running:
        canvas.fill((255, 255, 255))
        for key, (option_text, _) in options.items():
            option_color = selected_colour if key == 40 + selected_difficulty or (key == 45 and selected_play_side is SideEnum.WHITE) or (
                key == 46 and selected_play_side is SideEnum.BLACK) else unselected_colour
            square = pygame.draw.rect(
                canvas, (0, 0, 0), draw_square(pixel_size, key), 2)
            canvas.blit(pygame.TEXT_FONT.render(
                option_text, True, option_color), (square.left, square.top))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                current_mouse_location = pygame.mouse.get_pos()
                start_pressed_board_position = get_board_index(
                    current_mouse_location[0], current_mouse_location[1]
                )
                if start_pressed_board_position in options:
                    options[start_pressed_board_position][1]()

        pygame.display.update()

if __name__ == "__main__":
    
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.mixer.music.load("move.mp3")
    pygame.TEXT_FONT = pygame.font.SysFont('Arial', 25)
    pygame.PIECE_IMAGES = {}

    canvas_size = 512
    pixel_size = canvas_size // 8
    canvas = pygame.display.set_mode((canvas_size, canvas_size))
    load_images(pygame.PIECE_IMAGES)

    pygame.display.set_caption("CHESS")
    stalemate_screen(canvas, )
    draw_menu(canvas)
