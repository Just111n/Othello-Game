import math
from tkinter import *
import othello

# Constants
FONT = ("Verdana", 11, "bold")
HEIGHT = 500.0
WIDTH = 500.0
ROWS = othello.ROWS
COLS = othello.COLS
CELL_HEIGHT = HEIGHT / ROWS
CELL_WIDTH = WIDTH / COLS
PADDING = 10
PLAYERS = {"Black": othello.BLACK, "White": othello.WHITE, NONE: othello.EMPTY}
COLOUR_BLACK = "Black"
COLOUR_WHITE = "White"
COLOUR_GREEN = "Green"
COLOUR_RED = "Red"


class othelloGUI:
    # Initialises the class
    def __init__(self):
        self.game_state = othello.Othello()
        self.root = Tk()
        self.root.title("Othello")
        self.root.resizable(False, False)
        self.background = Canvas(self.root, bg=COLOUR_GREEN, width=WIDTH, height=HEIGHT)
        self.background.grid()
        self.init_score()
        self.update_board()
        self.background.bind('<Button-1>', self.update_on_click)

    # Create the gridlines
    def init_grid(self):
        for row in range(ROWS):
            self.background.create_line(0, row * CELL_HEIGHT, WIDTH, row * CELL_HEIGHT)
        for col in range(COLS):
            self.background.create_line(col * CELL_WIDTH, 0, col * CELL_WIDTH, HEIGHT)

    # Create Scoreboard on bottom
    def init_score(self):
        score_container = Frame(self.root)
        score_container.grid()

        # Use grid to split the scores nicely
        black_label = Frame(score_container, bg=COLOUR_WHITE)
        black_label.grid(row=0, column=0, columnspan=1, padx=PADDING, pady=PADDING)
        self.black_label = Label(master=black_label, text="Black ", bg=COLOUR_WHITE, justify=RIGHT, font=FONT,
                                 width=PADDING, height=1)
        self.black_label.pack()

        white_label = Frame(score_container, bg=COLOUR_WHITE)
        white_label.grid(row=0, column=2, columnspan=1, padx=PADDING, pady=PADDING)
        self.white_label = Label(master=white_label, text="White ", bg=COLOUR_WHITE, justify=RIGHT, font=FONT,
                                 width=PADDING, height=1)
        self.white_label.pack()

        black_score = Frame(score_container, bg=COLOUR_WHITE)
        black_score.grid(row=0, column=1, columnspan=1, padx=PADDING, pady=PADDING)
        self.black_score = Label(master=black_score, text="0", bg=COLOUR_WHITE, justify=RIGHT, font=FONT,
                                 width=PADDING, height=1)
        self.black_score.pack()

        white_score = Frame(score_container, bg=COLOUR_WHITE)
        white_score.grid(row=0, column=4, columnspan=1, padx=PADDING, pady=PADDING)
        self.white_score = Label(master=white_score, text="0", bg=COLOUR_WHITE, justify=RIGHT, font=FONT,
                                 width=PADDING, height=1)
        self.white_score.pack()

    # Update the values and placements of pieces on the board
    def update_board(self):
        # Delete all current pieces
        self.background.delete(ALL)
        # Redraw lines as they are also deleted when deleting the pieces
        self.init_grid()

        colors = {'1': "Black",
                  '0': "White"}

        # Update the score count
        self.white_score.configure(text=str(self.game_state.get_count(PLAYERS[COLOUR_WHITE])))
        self.black_score.configure(text=str(self.game_state.get_count(PLAYERS[COLOUR_BLACK])))

        # Fill the board with the current placements of pieces and place helper pieces for possible placements of pieces
        for r in range(ROWS):
            for c in range(COLS):
                if self.game_state.board[r][c] != othello.EMPTY:
                    self.background.create_oval(r * CELL_HEIGHT, c * CELL_WIDTH, (r + 1) * CELL_HEIGHT,
                                                (c + 1) * CELL_WIDTH, fill=colors[self.game_state.board[r][c]])
                elif self.game_state.is_valid_cell(r, c, self.game_state.player):
                    self.background.create_oval(r * CELL_HEIGHT + 15, c * CELL_WIDTH + 15, (r + 1) * CELL_HEIGHT - 15,
                                                (c + 1) * CELL_WIDTH - 15, fill=COLOUR_RED)

    # Use update_board to update after every click and checks if game over
    def update_on_click(self, event):
        row = math.floor(event.x // CELL_HEIGHT)
        col = math.floor(event.y // CELL_WIDTH)

        # Attempt to place a piece in the backend and update visually
        self.game_state.play(row, col)
        self.update_board()

        # Check if game over and display winner
        if self.game_state.game_over():
            winner = self.game_state.winner()
            win_text = ""
            if winner == PLAYERS[NONE]:
                win_text = "Tie!"
            elif winner == PLAYERS[COLOUR_BLACK]:
                win_text = "Black Wins!"
            elif winner == PLAYERS[COLOUR_WHITE]:
                win_text = "White Wins!"

            winner_container = Frame(self.root)
            winner_container.grid()

            winner_label = Frame(winner_container, bg=COLOUR_WHITE)
            winner_label.grid(row=0, column=0, columnspan=1, padx=PADDING, pady=PADDING)
            self.winner_label = Label(master=winner_label, text=win_text, bg=COLOUR_WHITE, justify=RIGHT,
                                      font=FONT, width=PADDING, height=1)
            self.winner_label.pack()


if __name__ == '__main__':
    othelloGUI().root.mainloop()
