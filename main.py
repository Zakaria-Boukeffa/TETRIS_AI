import tkinter as tk
from tetris import TetrisGame
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR

def main():
    """
    Main entry point for the Tetris game application.
    Sets up the tkinter root window and initializes the TetrisGame.
    """
    # Create the main window
    root = tk.Tk()
    root.title("Two-Player Tetris: Human vs AI")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.resizable(False, False)
    root.configure(bg=BACKGROUND_COLOR)
    
    # Create the game instance
    game = TetrisGame(root)
    
    # Start the game
    game.start()
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()