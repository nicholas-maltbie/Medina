"""This is the main file that allows a user to interact with the project
via a graphical user interface"""
import tkinter as tk
from tkinter import PhotoImage
from tkinter import font
import Game
import Player
import Board
import Tile
import BoardCanvas
import threading
import Agent
import HumanAgent
import Score

title_font = None
normal_font = None

def make_base_panel():
    """Makes a base panel with global attributes"""
    window = tk.Tk()
    window.title("Medina")
    img = PhotoImage(file='Assets/icon.gif')
    window.tk.call('wm', 'iconphoto', window._w, img)
    return window

def new_game_panel(parent=None):
    """Creates a new game panel"""
    if parent != None:
        parent.destroy()
    num_players = 4
    game_panel = make_base_panel()
    error_str = tk.Label(text="Press 'start' to start the game")
    player_values = {}
    def start_game():
        """Starts a game based on values in player_values"""
        colors = [player_values[(num, 'color')]() for num in range(num_players)]
        if len(colors) != len(set(colors)):
            error_str.configure(text="Two players cannot have the same color")
            return
        names = [player_values[(num, 'name')]() for num in range(num_players)]
        if len(names) != len(set(names)):
            error_str.configure(text="Two players cannot have the same name")
            return
        players = [Player.make_player(names[i], num_players, colors[i]) for i in range(num_players)]
        board = Board.make_board(11, 16)
        tile_supply = Tile.get_all_tiles()

        grid = BoardCanvas.GRID_SIZE
        gap = BoardCanvas.GRID_GAP
        num_humans = len([0 for num in range(num_players) if player_values[(num, 'type')]() == 'Human'])
        additional_x = 0
        if num_humans > 0:
            additional_x = grid * 7 + gap * 8

        game_panel.destroy()

        board_canvas = BoardCanvas.BoardCanvas(board, tile_supply, additional_x=additional_x)
        board_canvas.setup()

        board_canvas.title("Medina")
        img = PhotoImage(file='Assets/icon.gif')
        board_canvas.tk.call('wm', 'iconphoto', board_canvas._w, img)

        def play_game(board_canvas, board, tile_supply, players):
            random_agent = Agent.get_random_agent()
            human_agent = None
            if num_humans > 0:
                human_agent = HumanAgent.HumanAgent(board_canvas, board, tile_supply, 0, players).human_decision
            agents = []
            for num in range(num_players):
                if player_values[(num, 'type')]() == 'Human':
                    agents.append(human_agent)
                elif player_values[(num, 'type')]() == "Random":
                    agents.append(random_agent)

            scores, board, players, tile_supply = Game.play_game(board_canvas, board,
                players, tile_supply, agents)
            Score.displaySimpleScore(scores)

        thread = threading.Thread(target = play_game, args=[board_canvas, board, tile_supply, players])
        thread.daemon = True
        thread.start()

        board_canvas.mainloop()
        main_panel()

    def make_player_panel(row, default_name = "Name", default_type = "Random", default_color = "Blue"):
        """Makes a player panel"""
        tk.Label(text="Player " + str(row + 1) + ")").grid(row=row, column = 0, pady = 10)

        playerVar = tk.StringVar(game_panel)
        playerVar.set(default_type) # initial value
        option = tk.OptionMenu(game_panel, playerVar, "Human", "Random")
        option.grid(row = row, column = 2, padx = 5, ipadx = 5)
        player_values[(row, 'type')] = playerVar.get

        colorVar = tk.StringVar(game_panel)
        colorVar.set(default_color)
        color = tk.OptionMenu(game_panel, colorVar, "Blue", "Green", "Yello", "Red")
        color.grid(row = row, column = 3)
        player_values[(row, 'color')] = colorVar.get

        name = tk.Entry(game_panel)
        name.insert(0, str(default_name))
        name.grid(row = row, column = 1)
        player_values[(row, 'name')] = name.get

    names_iter = iter(["Nick", "Erin", "Brian", "Zach"])
    type_iter = iter(["Human", "Random", "Random", "Random"])
    color_iter = iter(['Blue', 'Green', 'Yellow', 'Red'])
    for i in range(4):
        make_player_panel(i, default_name=next(names_iter), default_type = next(type_iter),
                default_color = next(color_iter))

    back = tk.Button(text = "Back")
    back.grid(row = 4, column = 0,sticky='w')
    back.bind("<Button-1>", lambda event: main_panel(game_panel))

    error_str.grid(row = 4, column = 1, columnspan = 2)

    start = tk.Button(text = "Start")
    start.grid(row = 4, column = 3, stick = 'e')
    start.bind("<Button-1>", lambda event: start_game())

    game_panel.mainloop()

def main_panel(parent=None):
    """Creates the main panel"""
    if parent != None:
        parent.destroy()
    window = make_base_panel()
    window.geometry("200x200")
    title_font = font.Font(family='Helvetica', size=36, weight='bold')
    normal_font = font.Font(family='Helvetica', size=16, weight='normal')

    title = tk.Label(window, text="Medina", font = title_font)
    title.pack(fill = 'both', expand = True)
    title.pack(pady = 10)

    play_game = tk.Button(window, text= "Play Game", font = normal_font)
    play_game.bind("<Button-1>", lambda event: new_game_panel(window));
    play_game.pack(pady = 10)

    exit = tk.Button(window, text="Exit", font = normal_font)
    exit.bind("<Button-1>", lambda event: window.destroy())
    exit.pack(pady = 10)

    window.mainloop()

def main():
    main_panel()

if __name__ == "__main__":
    main()
