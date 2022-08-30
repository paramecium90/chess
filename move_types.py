def move_straight_cells(x, y):
    right_path = [[x, i+y] for i in range(1, 8) if i+y < 8]
    left_path = [[x, y-i] for i in range(1, 8) if y-i >= 0]
    up_path = [[x-i, y] for i in range(1, 8) if x-i >= 0]
    down_path = [[x+i, y] for i in range(1, 8) if i+x < 8]
    paths = [right_path, left_path, up_path, down_path]
    return paths


def move_diagonaly_cells(x, y):
    right_up_path = [[x-i, i+y] for i in range(1, 8) if i+y < 8 and x-i >= 0]
    right_down_path = [[x+i, i+y] for i in range(1, 8) if i+y < 8 and x+i < 8]
    left_down_path = [[x+i, y-i] for i in range(1, 8) if y-i >= 0 and x+i < 8]
    left_up_path = [[x-i, y-i] for i in range(1, 8) if x-i >= 0 and y-i >= 0]
    paths = [right_up_path, right_down_path, left_down_path, left_up_path]
    return paths


def move_knight_cells(x, y):
    cells = [[x+2, y+1], [x+2, y-1], [x-2, y+1], [x-2, y-1],
             [x+1, y+2], [x+1, y-2], [x-1, y+2], [x-1, y-2]]
    cells = [cell for cell in cells if (
        cell[0] >= 0 and cell[0] < 8) and (cell[1] >= 0 and cell[1] < 8)]

    # print(cells)
    return cells


def move_king_cells(x, y):
    cells = [[x-1, y], [x-1, y+1], [x, y+1], [x+1, y+1],
             [x+1, y], [x+1, y-1], [x, y-1], [x-1, y-1]]
    cells = [cell for cell in cells if (
        cell[0] >= 0 and cell[0] < 8) and (cell[1] >= 0 and cell[1] < 8)]

    # print(cells)
    return cells
