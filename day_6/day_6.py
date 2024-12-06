def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


class GridItems:
    EMPTY = "."
    WALL = "#"
    PLAYER_UP = "^"
    PLAYER_DOWN = "v"
    PLAYER_LEFT = "<"
    PLAYER_RIGHT = ">"
    VISITED_UP = "U"
    VISITED_UP_DOWN = "|"
    VISITED_DOWN = "D"
    VISITED_LEFT = "L"
    VISITED_LEFT_RIGHT = "-"
    VISITED_RIGHT = "R"


class GridCell:
    def __init__(self, status) -> None:
        self.status = status
        self.visited_by = []

    def visit(self, player_item):
        self.visited_by.append(self.status)
        self.status = get_visited_item(player_item, self.status)

    def is_visited_in_same_direction(self, player_item):
        return get_visited_item(player_item, self.status) in self.visited_by


def parse_content(content):
    grid = []
    player_position = None
    for row in content.split("\n"):
        row_list = []
        for item in row:
            if item == ".":
                row_list.append(GridCell(GridItems.EMPTY))
            elif item == "#":
                row_list.append(GridCell(GridItems.WALL))
            elif item == "^":
                player_position = (len(grid), len(row_list))
                row_list.append(GridCell(GridItems.PLAYER_UP))
            elif item == "v":
                row_list.append(GridCell(GridItems.PLAYER_DOWN))
            elif item == "<":
                row_list.append(GridCell(GridItems.PLAYER_LEFT))
            elif item == ">":
                row_list.append(GridCell(GridItems.PLAYER_RIGHT))
        grid.append(row_list)
    return grid, player_position


def get_next_position(player_item, player_position):
    if player_item == GridItems.PLAYER_UP:
        return (player_position[0] - 1, player_position[1])
    elif player_item == GridItems.PLAYER_DOWN:
        return (player_position[0] + 1, player_position[1])
    elif player_item == GridItems.PLAYER_LEFT:
        return (player_position[0], player_position[1] - 1)
    elif player_item == GridItems.PLAYER_RIGHT:
        return (player_position[0], player_position[1] + 1)
    else:
        return None


def is_position_valid_to_move_to(grid, position):
    try:
        return grid[position[0]][position[1]] != GridItems.WALL
    except IndexError:
        print(position)
        print(len(grid), len(grid[position[0]]))
        raise Exception("Player is doing something wrong")


def is_position_in_grid(grid, position):
    return (
        position[0] >= 0
        and position[0] < len(grid)
        and position[1] >= 0
        and position[1] < len(grid[0])
    )


def turn_player_right(player_item):
    if player_item == GridItems.PLAYER_UP:
        return GridItems.PLAYER_RIGHT
    elif player_item == GridItems.PLAYER_RIGHT:
        return GridItems.PLAYER_DOWN
    elif player_item == GridItems.PLAYER_DOWN:
        return GridItems.PLAYER_LEFT
    elif player_item == GridItems.PLAYER_LEFT:
        return GridItems.PLAYER_UP


def get_visited_item(player_item, current_item):
    if current_item == GridItems.VISITED_UP:
        if player_item == GridItems.PLAYER_DOWN:
            return GridItems.VISITED_UP_DOWN
    if current_item == GridItems.VISITED_DOWN:
        if player_item == GridItems.PLAYER_UP:
            return GridItems.VISITED_UP_DOWN
    if current_item == GridItems.VISITED_LEFT:
        if player_item == GridItems.PLAYER_RIGHT:
            return GridItems.VISITED_LEFT_RIGHT
    if current_item == GridItems.VISITED_RIGHT:
        if player_item == GridItems.PLAYER_LEFT:
            return GridItems.VISITED_LEFT_RIGHT

    if player_item == GridItems.PLAYER_UP:
        return GridItems.VISITED_UP
    elif player_item == GridItems.PLAYER_DOWN:
        return GridItems.VISITED_DOWN
    elif player_item == GridItems.PLAYER_LEFT:
        return GridItems.VISITED_LEFT
    elif player_item == GridItems.PLAYER_RIGHT:
        return GridItems.VISITED_RIGHT
    else:
        raise Exception("Player is doing something wrong")


def move_player(grid, player_position, player_position_before_move):
    player_item = grid[player_position[0]][player_position[1]]
    next_position = get_next_position(player_item, player_position)

    # try:
    #     print(
    #         is_visited_in_same_direction(
    #             player_item, grid[next_position[0]][next_position[1]]
    #         ),
    #         player_item,
    #         player_position_before_move,
    #         get_visited_item(player_item, player_position_before_move),
    #         grid[next_position[0]][next_position[1]],
    #     )
    # except Exception as e:
    #     pass

    if not is_position_in_grid(grid, next_position):
        grid[player_position[0]][player_position[1]] = get_visited_item(
            player_item, player_position_before_move
        )
        return grid, None, player_position_before_move, False

    if is_visited_in_same_direction(
        player_item, grid[next_position[0]][next_position[1]]
    ):
        return grid, None, player_position_before_move, True

    if not next_position:
        raise Exception("Player is doing something wrong")

    if is_position_valid_to_move_to(grid, next_position):
        next_position_before_move = grid[next_position[0]][next_position[1]]
        grid[player_position[0]][player_position[1]] = get_visited_item(
            player_item, player_position_before_move
        )
        grid[next_position[0]][next_position[1]] = player_item
        return grid, next_position, next_position_before_move, False
    else:
        grid[player_position[0]][player_position[1]] = turn_player_right(player_item)
        return grid, player_position, player_position_before_move, False


def is_visited(item):
    return item in [
        GridItems.VISITED_UP,
        GridItems.VISITED_DOWN,
        GridItems.VISITED_LEFT,
        GridItems.VISITED_RIGHT,
        GridItems.VISITED_UP_DOWN,
        GridItems.VISITED_LEFT_RIGHT,
    ]


def count_visited_positions(grid):
    count = 0
    for row in grid:
        for item in row:
            if is_visited(item):
                count += 1
    return count


def is_visited_in_same_direction(player_item, visited_item):
    if player_item == GridItems.PLAYER_UP and (
        visited_item == GridItems.VISITED_UP
        or visited_item == GridItems.VISITED_UP_DOWN
    ):
        return True
    elif player_item == GridItems.PLAYER_DOWN and (
        visited_item == GridItems.VISITED_DOWN
        or visited_item == GridItems.VISITED_UP_DOWN
    ):
        return True
    elif player_item == GridItems.PLAYER_LEFT and (
        visited_item == GridItems.VISITED_LEFT
        or visited_item == GridItems.VISITED_LEFT_RIGHT
    ):
        return True
    elif player_item == GridItems.PLAYER_RIGHT and (
        visited_item == GridItems.VISITED_RIGHT
        or visited_item == GridItems.VISITED_LEFT_RIGHT
    ):
        return True
    else:
        return False


# content = read_file("samples/sample_1.txt")
content = read_file("samples/challange.txt")
grid, player_position = parse_content(content)
while True:
    grid, player_position, _, _ = move_player(
        grid, player_position, GridItems.VISITED_UP
    )
    if not player_position:
        break

print(count_visited_positions(grid))
for row in grid:
    print("".join(row))

visited_positions = []
for i, row in enumerate(grid):
    for j, item in enumerate(row):
        if is_visited(item):
            visited_positions.append((i, j))

grid, player_position = parse_content(content)

# exclude the starting position
count_valid_paths = 0
visited_positions.pop(visited_positions.index(player_position))
for position in visited_positions:
    print(position)
    grid, player_position = parse_content(content)
    grid[position[0]][position[1]] = GridItems.WALL
    previous_position = GridItems.VISITED_UP
    while True:
        grid, player_position, previous_position, is_looped = move_player(
            grid, player_position, previous_position
        )
        # print(player_position)
        if is_looped:
            count_valid_paths += 1
            break

        if not player_position:
            break


print(count_valid_paths)
