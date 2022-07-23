# Constants
EMPTY = '.'
BLACK = '1'
WHITE = '0'
ROWS = 8
COLS = 8


class Othello:
    # Initialise the class
    def __init__(self):
        self.board = self.new_board()
        self.player = BLACK

    def new_board(self):
        board = []

        # Create Board
        # board = [[EMPTY for column in range(COLS)]for row in range(ROWS)]
        for row in range(ROWS):
            board.append([])
            for col in range(COLS):
                board[row].append(EMPTY)
        
        # Place pieces at center
        board[3][3] = WHITE
        board[4][4] = WHITE
        board[3][4] = BLACK
        board[4][3] = BLACK

        return board

    # Attempt to place piece on row and col
    def play(self, row, col):
        # Check that the current player can play else switch player
        if not self.can_play(self.player):
            self.player = self.opponent(self.player)

        # Check if the cell selected is within the possible moves of the player
        elif self.is_valid_cell(row,  col, self.player):
            # Place the piece on the selected cell
            for position in self.check_surrounding(row, col, self.player):
                # Flip all the cells of the opponent between selected cell and the player cell
                self.execute_move(row, col, position[0], position[1], self.player)
            self.board[row][col] = self.player
            # Switch turn when all actions are executed
            self.player = self.opponent(self.player)
        # If invalid cell selected raise an error
        else:
            raise InvalidSpaceException

    # Gets possible moves by current player
    def is_valid_cell(self, row, col, player):
        # Check whether the cell is within the board and is empty
        self.check_space(row, col)
        # Get the relative positions of the opposing pieces in relation to the selected cell
        surrounding_opponents_positions = self.check_surrounding(row, col, player)

        # Traverse in the directions of the opposing pieces and check if there is another piece from the current player
        for position in surrounding_opponents_positions:
            if self.is_valid_direction(row, col, position[0], position[1], player):
                return True
        # If all directions not valid cell is not valid cell
        return False

    # Check whether either player can still play
    def game_over(self):
        return not self.can_play(BLACK) and not self.can_play(WHITE)

    # Counts number of pieces and returns the winner
    def winner(self):
        num_black = self.get_count(BLACK)
        num_white = self.get_count(WHITE)

        if num_black == num_white:
            return EMPTY
        elif num_black > num_white:
            return BLACK
        elif num_white > num_black:
            return WHITE

    # Counts number of pieces from the player specified
    def get_count(self, player):
        count = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == player:
                    count += 1
        return count

    # Check if cell selected is within the board
    def is_within_boundary(self, row, col):
        return (0 <= row < ROWS) and (0 <= col < COLS)

    #  Check if space is empty and within the board
    def check_space(self, row, col):
        if self.is_within_boundary(row, col) and self.board[row][col] != EMPTY:
            raise InvalidSpaceException

    # Returns the other player
    def opponent(self, player):
        swap = {BLACK: WHITE,
                WHITE: BLACK}
        return swap[player]

    #  Returns the relative positions of opponent pieces around the selected cell
    def check_surrounding(self, row, col, player):
        opponent_relative_positions = []
        for r in range(-1, 2):
            for c in range(-1, 2):
                if self.is_within_boundary(row + r, col + c):
                    if self.board[row + r][col + c] == self.opponent(player):
                        opponent_relative_positions.append((r, c))
        return opponent_relative_positions

    # Checks if there is a cell from the specified player at other end of the selected cell
    def is_valid_direction(self, row, col, r, c, player):
        current_row = row + r
        current_col = col + c

        # Loop until reach same player cell
        while self.board[current_row][current_col] != player:
            current_row += r
            current_col += c

            # Not valid when reach out of bounds or reach empty cell
            if not self.is_within_boundary(current_row, current_col) or self.board[current_row][current_col] == EMPTY:
                return False
        return True

    # Flip all the opponent cells in the direction is valid until the player's own cell
    def execute_move(self, row, col, r, c, player):
        if self.is_valid_direction(row, col, r, c, player):
            current_row = row + r
            current_col = col + c

            # Loop as long as cell belongs to the opponent, move along r and c and flip the cell
            while self.board[current_row][current_col] == self.opponent(player):
                self.board[current_row][current_col] = self.opponent(self.board[current_row][current_col])
                current_row += r
                current_col += c

    # Check if player can still place a piece
    def can_play(self, player):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == EMPTY:
                    if self.is_valid_cell(row, col, player):
                        return True
        return False


class InvalidSpaceException(Exception):
    pass
