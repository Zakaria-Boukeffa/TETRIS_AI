import tkinter as tk
import random
import time
from constants import *
from ai import TetrisAI
from score import ScoreManager

class TetrisGame:
    def __init__(self, master):
        """Initialize the Tetris game with two boards - human and AI"""
        self.master = master
        self.score_manager = ScoreManager()
        
        self.human_next_piece = None
        self.ai_next_piece = None
        
        # Create the game canvas
        self.canvas = tk.Canvas(
            master, 
            width=WINDOW_WIDTH, 
            height=WINDOW_HEIGHT, 
            bg=BACKGROUND_COLOR
        )
        self.canvas.pack()
        
        # Initialize game state variables
        self.is_running = False
        self.paused = False
        self.game_over = False
        self.using_alt_colors = False
        self.color_change_timer = None
        self.slowdown_timer = None
        
        # Initialize human board
        self.human_board = self._create_empty_board()
        self.human_current_piece = None
        self.human_current_shape = None
        self.human_current_x = 0
        self.human_current_y = 0
        self.human_fall_speed = INITIAL_SPEED
        self.human_is_slowed = False
        
        # Initialize AI board
        self.ai_board = self._create_empty_board()
        self.ai_current_piece = None
        self.ai_current_shape = None
        self.ai_current_x = 0
        self.ai_current_y = 0
        self.ai_fall_speed = INITIAL_SPEED
        self.ai_is_slowed = False
        
        # Create AI player
        self.ai = TetrisAI(self)
        
        # Set up key bindings for human player
        self.master.bind("<Left>", self._move_left)
        self.master.bind("<Right>", self._move_right)
        self.master.bind("<Down>", self._move_down)
        self.master.bind("<Up>", self._rotate)
        self.master.bind("<space>", self._hard_drop)
        self.master.bind("p", self._toggle_pause)
        
        # Create UI elements
        self._create_ui()
        
    def _create_empty_board(self):
        """Create an empty Tetris board"""
        return [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    
    def _create_ui(self):
        """Create the game's UI elements"""
        # Draw borders for both boards
        self._draw_board_border(HUMAN_BOARD_X, BOARD_Y, "Human Player")
        self._draw_board_border(AI_BOARD_X, BOARD_Y, "AI Player")
        
        # Score displays
        self.human_score_text = self.canvas.create_text(
            HUMAN_BOARD_X + (BOARD_WIDTH * BLOCK_SIZE) // 2,
            BOARD_Y + BOARD_HEIGHT * BLOCK_SIZE + 30,
            text="Score: 0",
            font=("Arial", 14),
            fill=TEXT_COLOR
        )
        
        self.ai_score_text = self.canvas.create_text(
            AI_BOARD_X + (BOARD_WIDTH * BLOCK_SIZE) // 2,
            BOARD_Y + BOARD_HEIGHT * BLOCK_SIZE + 50,
            text="Score: 0",
            font=("Arial", 14),
            fill=TEXT_COLOR
        )
        
        # Next piece preview labels
        self.canvas.create_text(
            HUMAN_BOARD_X + (BOARD_WIDTH * BLOCK_SIZE) // 2,
            BOARD_Y - 30,
            text="Next Piece:",
            font=("Arial", 12),
            fill=TEXT_COLOR
        )
        
        self.canvas.create_text(
            AI_BOARD_X + (BOARD_WIDTH * BLOCK_SIZE) // 2,
            BOARD_Y - 30,
            text="Next Piece:",
            font=("Arial", 12),
            fill=TEXT_COLOR
        )
        
        # Status message display (for bonuses, etc.)
        self.status_text = self.canvas.create_text(
            WINDOW_WIDTH // 2,
            BOARD_Y + BOARD_HEIGHT * BLOCK_SIZE + 90,
            text="",
            font=("Arial", 14, "bold"),
            fill=BONUS_TEXT_COLOR
        )
        
        # Help text for controls
        controls_text = "Controls: ← → Move | ↑ Rotate | ↓ Soft Drop | Space Hard Drop | P Pause"
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT - 30,
            text=controls_text,
            font=("Arial", 10),
            fill=TEXT_COLOR
        )
    
    def _draw_board_border(self, x, y, title):
        """Draw a border around a game board with a title"""
        # Board title
        self.canvas.create_text(
            x + (BOARD_WIDTH * BLOCK_SIZE) // 2,
            y - 60,
            text=title,
            font=("Arial", 16, "bold"),
            fill=TEXT_COLOR
        )
        
        # Board border
        self.canvas.create_rectangle(
            x - 2, y - 2,
            x + BOARD_WIDTH * BLOCK_SIZE + 2,
            y + BOARD_HEIGHT * BLOCK_SIZE + 2,
            outline=BORDER_COLOR,
            width=2
        )
    
    def start(self):
        """Start the game"""
        if not self.is_running:
            self.is_running = True
            self.game_over = False
            
            # Reset scores
            self.score_manager.reset_scores()
            self._update_score_display()
            
            # Create initial pieces
            self._new_human_piece()
            self._new_ai_piece()
            
            # Start color change timer
            self._schedule_color_change()
            
            # Start game loops
            self._human_game_loop()
            self._ai_game_loop()
    
    def _schedule_color_change(self):
        """Schedule the color change special effect"""
        self.master.after(COLOR_CHANGE_INTERVAL, self._start_color_change)
    
    def _start_color_change(self):
        """Start the color change effect"""
        if not self.game_over:
            self.using_alt_colors = True
            self._show_status_message("Color Change Activated!")
            self._redraw_boards()
            
            # Schedule end of color change
            self.color_change_timer = self.master.after(COLOR_CHANGE_DURATION, self._end_color_change)
            
            # Schedule next color change
            self._schedule_color_change()
    
    def _end_color_change(self):
        """End the color change effect"""
        if not self.game_over:
            self.using_alt_colors = False
            self._clear_status_message()
            self._redraw_boards()
    
    def _activate_slowdown(self, is_human):
        """Activate the slowdown bonus for a player"""
        if is_human:
            self.human_is_slowed = True
            self.human_fall_speed = int(self.human_fall_speed / SLOWDOWN_PERCENTAGE)
            # Schedule end of slowdown
            self.master.after(SLOWDOWN_BONUS_DURATION, self._end_human_slowdown)
        else:
            self.ai_is_slowed = True
            self.ai_fall_speed = int(self.ai_fall_speed / SLOWDOWN_PERCENTAGE)
            # Schedule end of slowdown
            self.master.after(SLOWDOWN_BONUS_DURATION, self._end_ai_slowdown)
        
        self._show_status_message(f"{'Human' if is_human else 'AI'} gets a Slowdown Bonus!")
    
    def _end_human_slowdown(self):
        """End the slowdown bonus for the human player"""
        if not self.game_over:
            self.human_is_slowed = False
            self.human_fall_speed = int(self.human_fall_speed * SLOWDOWN_PERCENTAGE)
            self._clear_status_message()
    
    def _end_ai_slowdown(self):
        """End the slowdown bonus for the AI player"""
        if not self.game_over:
            self.ai_is_slowed = False
            self.ai_fall_speed = int(self.ai_fall_speed * SLOWDOWN_PERCENTAGE)
            self._clear_status_message()
    
    def _show_status_message(self, message):
        """Display a status message on the screen"""
        self.canvas.itemconfig(self.status_text, text=message)
    
    def _clear_status_message(self):
        """Clear the status message"""
        self.canvas.itemconfig(self.status_text, text="")
    
    def _update_score_display(self):
        """Update the score displays for both players"""
        self.canvas.itemconfig(
            self.human_score_text,
            text=f"Score: {self.score_manager.get_human_score()}"
        )
        self.canvas.itemconfig(
            self.ai_score_text,
            text=f"Score: {self.score_manager.get_ai_score()}"
        )
    
    def _human_game_loop(self):
        """Main game loop for the human player"""
        if not self.paused and self.is_running and not self.game_over:
            if self._check_collision(self.human_board, self.human_current_piece, 
                                    self.human_current_x, self.human_current_y + 1):
                # Place the piece on the board and check for completed lines
                self._place_piece(self.human_board, self.human_current_piece, 
                                 self.human_current_x, self.human_current_y)
                lines_cleared = self._clear_lines(self.human_board)
                
                # Update score and check for special actions
                score_added = self.score_manager.update_human_score(lines_cleared)
                self._update_score_display()
                
                # Check for special rules
                self._check_special_rules(lines_cleared, score_added, True)
                
                # Create a new piece
                if not self._new_human_piece():
                    self._game_over()
                    return
            else:
                # Move the piece down
                self.human_current_y += 1
            
            # Redraw the board
            self._redraw_human_board()
            
            # Schedule the next loop iteration
            self.master.after(self.human_fall_speed, self._human_game_loop)
    
    def _ai_game_loop(self):
        """Main game loop for the AI player"""
        if not self.paused and self.is_running and not self.game_over:
            if self._check_collision(self.ai_board, self.ai_current_piece, 
                                    self.ai_current_x, self.ai_current_y + 1):
                # Place the piece on the board and check for completed lines
                self._place_piece(self.ai_board, self.ai_current_piece, 
                                 self.ai_current_x, self.ai_current_y)
                lines_cleared = self._clear_lines(self.ai_board)
                
                # Update score and check for special actions
                score_added = self.score_manager.update_ai_score(lines_cleared)
                self._update_score_display()
                
                # Check for special rules
                self._check_special_rules(lines_cleared, score_added, False)
                
                # Create a new piece
                if not self._new_ai_piece():
                    self._game_over()
                    return
                
                # Let the AI make its move
                self.master.after(AI_MOVE_DELAY, self._ai_make_move)
            else:
                # Move the piece down
                self.ai_current_y += 1
            
            # Redraw the board
            self._redraw_ai_board()
            
            # Schedule the next loop iteration
            self.master.after(self.ai_fall_speed, self._ai_game_loop)
    
    def _check_special_rules(self, lines_cleared, score_added, is_human):
        """Check and apply special rules based on game events"""
        human_score = self.score_manager.get_human_score()
        ai_score = self.score_manager.get_ai_score()
        
        # Surprise Gift: Clearing 2 lines grants the opponent an easy piece
        if lines_cleared == 2:
            self._show_status_message(f"Surprise Gift for {'AI' if is_human else 'Human'}!")
            # Next piece for opponent will be easy (I or O shape)
            if is_human:
                self.ai_next_piece_override = random.choice(['I', 'O'])
            else:
                self.human_next_piece_override = random.choice(['I', 'O'])
        
        # Slowdown Bonus: Every 1000 points, pieces fall 20% slower for 10 seconds
        current_score = human_score if is_human else ai_score
        if current_score // SLOWDOWN_BONUS_THRESHOLD > (current_score - score_added) // SLOWDOWN_BONUS_THRESHOLD:
            self._activate_slowdown(is_human)
        
        # Special Piece: Every 3000 points, a unique-shaped piece appears
        if current_score // SPECIAL_PIECE_THRESHOLD > (current_score - score_added) // SPECIAL_PIECE_THRESHOLD:
            if is_human:
                self.human_next_piece_override = 'SPECIAL'
                self._show_status_message("Special Piece Coming for Human!")
            else:
                self.ai_next_piece_override = 'SPECIAL'
                self._show_status_message("Special Piece Coming for AI!")
    
    def _ai_make_move(self):
        """Let the AI make its move"""
        if not self.paused and self.is_running and not self.game_over:
            # Get AI's recommended move
            best_x, best_rotation = self.ai.get_best_move(
                self.ai_board, 
                self.ai_current_piece, 
                self.ai_current_shape
            )
            
            # Apply rotations
            current_rotation = 0
            while current_rotation < best_rotation:
                new_piece = self._rotate_piece(self.ai_current_piece)
                if not self._check_collision(self.ai_board, new_piece, self.ai_current_x, self.ai_current_y):
                    self.ai_current_piece = new_piece
                current_rotation += 1
            
            # Move horizontally
            while self.ai_current_x < best_x:
                if not self._check_collision(self.ai_board, self.ai_current_piece, 
                                            self.ai_current_x + 1, self.ai_current_y):
                    self.ai_current_x += 1
                else:
                    break
            
            while self.ai_current_x > best_x:
                if not self._check_collision(self.ai_board, self.ai_current_piece, 
                                            self.ai_current_x - 1, self.ai_current_y):
                    self.ai_current_x -= 1
                else:
                    break
            
            # Redraw the board
            self._redraw_ai_board()
    
    def _new_human_piece(self):
        """Create a new piece for the human player"""
        # Check if there's an override (for special rules)
        if hasattr(self, 'human_next_piece_override') and self.human_next_piece_override:
            self.human_current_shape = self.human_next_piece_override
            del self.human_next_piece_override
        else:
            # Select a random tetromino
            self.human_current_shape = random.choice(list(SHAPES.keys()))
            # Don't randomly select the special piece
            while self.human_current_shape == 'SPECIAL':
                self.human_current_shape = random.choice(list(SHAPES.keys()))
        
        # Get the tetromino shape
        self.human_current_piece = SHAPES[self.human_current_shape][0]
        
        # Starting position
        self.human_current_x = BOARD_WIDTH // 2 - len(self.human_current_piece[0]) // 2
        self.human_current_y = 0
        
        # Check if the new piece can be placed
        if self._check_collision(self.human_board, self.human_current_piece, 
                               self.human_current_x, self.human_current_y):
            return False  # Game over
    
        
        return True
    
    def _new_ai_piece(self):
        """Create a new piece for the AI player"""
        # Check if there's an override (for special rules)
        if hasattr(self, 'ai_next_piece_override') and self.ai_next_piece_override:
            self.ai_current_shape = self.ai_next_piece_override
            del self.ai_next_piece_override
        else:
            # Select a random tetromino
            self.ai_current_shape = random.choice(list(SHAPES.keys()))
            # Don't randomly select the special piece
            while self.ai_current_shape == 'SPECIAL':
                self.ai_current_shape = random.choice(list(SHAPES.keys()))
        
        # Get the tetromino shape
        self.ai_current_piece = SHAPES[self.ai_current_shape][0]
        
        # Starting position
        self.ai_current_x = BOARD_WIDTH // 2 - len(self.ai_current_piece[0]) // 2
        self.ai_current_y = 0
        
        # Check if the new piece can be placed
        if self._check_collision(self.ai_board, self.ai_current_piece, 
                               self.ai_current_x, self.ai_current_y):
            return False  # Game over
        
        return True
    
    def _check_collision(self, board, piece, x, y):
        """Check if a piece collides with the board boundaries or other pieces"""
        for row in range(len(piece)):
            for col in range(len(piece[row])):
                if piece[row][col]:
                    # Check if piece is out of bounds
                    if (y + row >= BOARD_HEIGHT or 
                        x + col < 0 or 
                        x + col >= BOARD_WIDTH):
                        return True
                    
                    # Check if piece collides with another piece on the board
                    if y + row >= 0 and board[y + row][x + col]:
                        return True
        
        return False
    
    def _place_piece(self, board, piece, x, y):
        """Place a piece on the board"""
        for row in range(len(piece)):
            for col in range(len(piece[row])):
                if piece[row][col]:
                    if 0 <= y + row < BOARD_HEIGHT and 0 <= x + col < BOARD_WIDTH:
                        # Store the piece type along with the block
                        if isinstance(piece[row][col], int) and piece[row][col] == 1:
                            # For regular blocks
                            board[y + row][x + col] = 1
                        else:
                            # For special blocks
                            board[y + row][x + col] = piece[row][col]
    
    def _clear_lines(self, board):
        """Clear completed lines and return the number of lines cleared"""
        lines_cleared = 0
        y = BOARD_HEIGHT - 1
        while y >= 0:
            # Check if line is complete
            if all(board[y]):
                lines_cleared += 1
                # Move all lines above down
                for y_above in range(y, 0, -1):
                    for x in range(BOARD_WIDTH):
                        board[y_above][x] = board[y_above - 1][x]
                
                # Clear the top line
                for x in range(BOARD_WIDTH):
                    board[0][x] = 0
            else:
                y -= 1
        
        return lines_cleared
    
    def _rotate_piece(self, piece):
        """Rotate a piece 90 degrees clockwise"""
        rows = len(piece)
        cols = len(piece[0])
        
        # Create a new rotated piece
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        
        # Fill the rotated piece
        for row in range(rows):
            for col in range(cols):
                rotated[col][rows - 1 - row] = piece[row][col]
        
        return rotated
    
    def _redraw_boards(self):
        """Redraw both game boards"""
        self._redraw_human_board()
        self._redraw_ai_board()
    
    def _redraw_human_board(self):
        """Redraw the human player's board"""
        # Clear the existing board
        self.canvas.delete("human_board")
        
        # Draw the grid
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                x = HUMAN_BOARD_X + col * BLOCK_SIZE
                y = BOARD_Y + row * BLOCK_SIZE
                
                # Draw grid cell
                self.canvas.create_rectangle(
                    x, y, x + BLOCK_SIZE, y + BLOCK_SIZE,
                    outline=GRID_COLOR, width=1, tags="human_board"
                )
                
                # Draw blocks on the board
                if self.human_board[row][col]:
                    self.canvas.create_rectangle(
                        x, y, x + BLOCK_SIZE, y + BLOCK_SIZE,
                        fill=self._get_color(self.human_current_shape),
                        outline="", tags="human_board"
                    )
        
        # Draw the current piece
        if self.human_current_piece:
            for row in range(len(self.human_current_piece)):
                for col in range(len(self.human_current_piece[row])):
                    if self.human_current_piece[row][col]:
                        x = HUMAN_BOARD_X + (self.human_current_x + col) * BLOCK_SIZE
                        y = BOARD_Y + (self.human_current_y + row) * BLOCK_SIZE
                        
                        self.canvas.create_rectangle(
                            x, y, x + BLOCK_SIZE, y + BLOCK_SIZE,
                            fill=self._get_color(self.human_current_shape),
                            outline="white", tags="human_board"
                        )
    
    def _redraw_ai_board(self):
        """Redraw the AI player's board"""
        # Clear the existing board
        self.canvas.delete("ai_board")
        
        # Draw the grid
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                x = AI_BOARD_X + col * BLOCK_SIZE
                y = BOARD_Y + row * BLOCK_SIZE
                
                # Draw grid cell
                self.canvas.create_rectangle(
                    x, y, x + BLOCK_SIZE, y + BLOCK_SIZE,
                    outline=GRID_COLOR, width=1, tags="ai_board"
                )
                
                # Draw blocks on the board
                if self.ai_board[row][col]:
                    self.canvas.create_rectangle(
                        x, y, x + BLOCK_SIZE, y + BLOCK_SIZE,
                        fill=self._get_color(self.ai_current_shape),
                        outline="", tags="ai_board"
                    )
        
        # Draw the current piece
        if self.ai_current_piece:
            for row in range(len(self.ai_current_piece)):
                for col in range(len(self.ai_current_piece[row])):
                    if self.ai_current_piece[row][col]:
                        x = AI_BOARD_X + (self.ai_current_x + col) * BLOCK_SIZE
                        y = BOARD_Y + (self.ai_current_y + row) * BLOCK_SIZE
                        
                        self.canvas.create_rectangle(
                            x, y, x + BLOCK_SIZE, y + BLOCK_SIZE,
                            fill=self._get_color(self.ai_current_shape),
                            outline="white", tags="ai_board"
                        )
    
    def _get_color(self, shape_key):
        """Get the color for a tetromino shape"""
        if self.using_alt_colors:
            return ALT_PIECE_COLORS.get(shape_key, "#FFFFFF")
        else:
            return PIECE_COLORS.get(shape_key, "#FFFFFF")
    
    def _move_left(self, event):
        """Move the human player's piece left"""
        if not self.paused and self.is_running and not self.game_over:
            if not self._check_collision(self.human_board, self.human_current_piece, 
                                        self.human_current_x - 1, self.human_current_y):
                self.human_current_x -= 1
                self._redraw_human_board()
    
    def _move_right(self, event):
        """Move the human player's piece right"""
        if not self.paused and self.is_running and not self.game_over:
            if not self._check_collision(self.human_board, self.human_current_piece, 
                                        self.human_current_x + 1, self.human_current_y):
                self.human_current_x += 1
                self._redraw_human_board()
    
    def _move_down(self, event):
        """Move the human player's piece down (soft drop)"""
        if not self.paused and self.is_running and not self.game_over:
            if not self._check_collision(self.human_board, self.human_current_piece, 
                                        self.human_current_x, self.human_current_y + 1):
                self.human_current_y += 1
                self._redraw_human_board()
    
    def _rotate(self, event):
        """Rotate the human player's piece"""
        if not self.paused and self.is_running and not self.game_over:
            new_piece = self._rotate_piece(self.human_current_piece)
            if not self._check_collision(self.human_board, new_piece, 
                                        self.human_current_x, self.human_current_y):
                self.human_current_piece = new_piece
                self._redraw_human_board()
    
    def _hard_drop(self, event):
        """Instantly drop the human player's piece to the bottom"""
        if not self.paused and self.is_running and not self.game_over:
            while not self._check_collision(self.human_board, self.human_current_piece, 
                                           self.human_current_x, self.human_current_y + 1):
                self.human_current_y += 1
            
            self._redraw_human_board()
    
    def _toggle_pause(self, event):
        """Pause or unpause the game"""
        self.paused = not self.paused
        
        if self.paused:
            self._show_status_message("Game Paused - Press 'P' to Resume")
        else:
            self._clear_status_message()
            # Restart the game loops if unpausing
            self._human_game_loop()
            self._ai_game_loop()
    
    def _game_over(self):
        """End the game"""
        self.game_over = True
        self.is_running = False
        
        # Display game over message and winner
        human_score = self.score_manager.get_human_score()
        ai_score = self.score_manager.get_ai_score()
        
        if human_score > ai_score:
            winner = "Human Wins!"
        elif ai_score > human_score:
            winner = "AI Wins!"
        else:
            winner = "It's a Tie!"
        
        self._show_status_message(f"Game Over! {winner} Press 'R' to Restart")
        
        # Add restart binding
        self.master.bind("r", self._restart_game)
    
    def _restart_game(self, event=None):
        """Restart the game"""
        # Reset boards
        self.human_board = self._create_empty_board()
        self.ai_board = self._create_empty_board()
        
        # Cancel any pending timers
        if self.color_change_timer:
            self.master.after_cancel(self.color_change_timer)
        if self.slowdown_timer:
            self.master.after_cancel(self.slowdown_timer)
        
        # Reset game state
        self.paused = False
        self.game_over = False
        self.using_alt_colors = False
        self.human_is_slowed = False
        self.ai_is_slowed = False
        self.human_fall_speed = INITIAL_SPEED
        self.ai_fall_speed = INITIAL_SPEED
        
        # Clear any status messages
        self._clear_status_message()
        
        # Start the game
        self.start()