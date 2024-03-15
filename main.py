import pygame
from Engine import ChessEngine as Chess
from ChessUtility import indexToRF, rfToIndex
from Enums.PieceEnum import PieceEnum
from Enums.SideEnum import SideEnum


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
        text = str(board[i]) if board[i] is not None else ""
        canvas.blit(
            pygame.font.SysFont("Arial", 25).render(text, True, (0, 0, 0)), square
        )


if __name__ == "__main__":
    instance = Chess()
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("move.mp3")

    canvas_size = 512
    pixel_size = canvas_size // 8
    canvas = pygame.display.set_mode((canvas_size, canvas_size))

    pygame.display.set_caption("CHESS")
    exit = False

    previous_pressed_state = False
    start_pressed_board_position = 0
    draw_board(canvas, instance.board)

    while not exit:
        for event in pygame.event.get():
            if instance.SideToPlay is SideEnum.BLACK:
                move = instance.search_moves()
                instance.makeMove(move)
                draw_board(canvas, instance.board)
                pygame.draw.rect(canvas, (255,0,0), draw_square(pixel_size, move.startPosition), 5)
                pygame.draw.rect(canvas, (255,0,0), draw_square(pixel_size, move.endPosition), 5)
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
                        pygame.draw.rect(canvas, (0,255,0), draw_square(pixel_size, moves.endPosition), 5)
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
                        f"{indexToRF(move.startPosition)}{indexToRF(move.endPosition)}"
                    )
                if toMake not in rf_moves:
                    continue
                instance.makeMove(all_moves[rf_moves.index(toMake)])
                draw_board(canvas, instance.board)
                pygame.mixer.music.play()
                print(instance.displayBoard())
        if instance.checkmated:
            exit=True

        pygame.display.update()
