import pygame
from Engine import ChessEngine as Chess
from ChessUtility import indexToRF, rfToIndex
from Enums.PieceEnum import PieceEnum
from Enums.SideEnum import SideEnum


def get_board_index(x, y):
    column = x // pixel_size
    row = y // pixel_size
    return column + 8 * row


def draw_board(canvas, board):
    canvas.fill((255, 255, 255))
    squares: list[pygame.Rect]= []
    # Draw squares
    for i in range(64):
        currentRow = i // 8
        currentColumn = i % 8

        odd = (i + currentRow) % 2
        color = (255, 255, 255) if odd else (220, 220, 220)
        ays = pygame.draw.rect(
            canvas,
            color,
            [
                currentColumn * pixel_size,
                currentRow * pixel_size,
                pixel_size,
                pixel_size,
            ],
        )
        squares.append(ays)

    for i, square in enumerate(squares):
        text = str(board[i]) if board[i] is not None else ""
        canvas.blit(
            pygame.font.SysFont("Arial", 25).render(text, True, (0, 0, 0)), square
        )


if __name__ == "__main__":
    instance = Chess()
    pygame.init()

    canvas_size = 1024
    pixel_size = canvas_size // 8
    canvas = pygame.display.set_mode((canvas_size, canvas_size))

    pygame.display.set_caption("CHESS")
    exit = False

    previous_pressed_state = False
    start_pressed_board_position = 0
    while not exit:
        draw_board(canvas, instance.board)
        for event in pygame.event.get():
            current_mouse_location = pygame.mouse.get_pos()

            if event.type is pygame.QUIT:
                exit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_pressed_board_position = get_board_index(
                    current_mouse_location[0], current_mouse_location[1]
                )
            if event.type == pygame.MOUSEBUTTONUP:
                current_board_position = get_board_index(
                    current_mouse_location[0], current_mouse_location[1]
                )
                toMake = f"{indexToRF(start_pressed_board_position)}{indexToRF(current_board_position)}"
                all_moves = instance.generate_all_moves()
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
                print(instance.displayBoard())
        if instance.checkmated:
            exit=True

        pygame.display.update()

    # while not instance.checkmated:

    #     print("\nTotal amount of moves:", total)

    #     toMake = input("Enter your move: ")

    #     if toMake == "-1":
    #         instance.unmakeMove()
    #         continue

    #     # Check if move in allowed moves list
    #     if toMake not in rf_moves:
    #         # if not in the list, ask for move again by skipping make move logic
    #         continue

    #     instance.makeMove(all_moves[rf_moves.index(toMake)])
