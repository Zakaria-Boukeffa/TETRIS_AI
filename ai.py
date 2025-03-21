"""
AI player logic for the Tetris game.
Implements a simple AI that decides piece placement.
"""

import random
from constants import BOARD_WIDTH, BOARD_HEIGHT, AI_THINKING_DEPTH

class TetrisAI:
    def __init__(self, game):
        """Initialize the Tetris AI with a reference to the game"""
        self.game = game
    
    def get_best_move(self, board, piece, shape):
        """
        Determine the best move (position and rotation) for the current piece
        Returns the best x position and rotation
        """
        best_score = float('-inf')
        best_x = 0
        best_rotation = 0
        
        # Try all possible rotations
        rotations = 4  # Maximum 4 rotations (0°, 90°, 180°, 270°)
        current_piece = piece
        
        for rotation in range(rotations):
            # Get width of the current piece orientation
            piece_width = len(current_piece[0])
            
            # Try all possible x positions
            for x in range(BOARD_WIDTH - piece_width + 1):
                # Create a copy of the board for simulation
                test_board = [row[:] for row in board]
                
                # Find the y position where the piece would land
                y = 0
                while y < BOARD_HEIGHT and not self._check_collision(test_board, current_piece, x, y + 1):
                    y += 1
                
                # Place the piece on the test board
                self._place_piece(test_board, current_piece, x, y)
                
                # Evaluate the board
                score = self._evaluate_board(test_board)
                
                # Add some randomness to make the AI less predictable
                score += random.uniform(-0.5, 0.5)
                
                # Update best move if this one is better
                if score > best_score:
                    best_score = score
                    best_x = x
                    best_rotation = rotation
            
            # Rotate the piece for the next iteration
            current_piece = self._rotate_piece(current_piece)
        
        return best_x, best_rotation
    
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
        """Place a piece on the board (for simulation purposes)"""
        for row in range(len(piece)):
            for col in range(len(piece[row])):
                if piece[row][col] and 0 <= y + row < BOARD_HEIGHT and 0 <= x + col < BOARD_WIDTH:
                    board[y + row][x + col] = 1
    
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
    
    def _evaluate_board(self, board):
        """
        Evaluate a board position using a weighted sum of features
        Higher score means better position
        """
        # Count completed lines
        completed_lines = self._count_completed_lines(board)
        
        # Calculate height of each column
        heights = self._get_column_heights(board)
        
        # Calculate bumpiness (sum of height differences between adjacent columns)
        bumpiness = self._get_bumpiness(heights)
        
        # Count holes (empty cells with at least one filled cell above)
        holes = self._count_holes(board, heights)
        
        # Calculate aggregate height (sum of all column heights)
        aggregate_height = sum(heights)
        
        # Weights for each feature
        weights = {
            'completed_lines': 8.0,
            'holes': -6,
            'bumpiness': -2.5,
            'aggregate_height': -0.8
        }
        
        # Calculate weighted sum
        score = (
            weights['completed_lines'] * completed_lines +
            weights['holes'] * holes +
            weights['bumpiness'] * bumpiness +
            weights['aggregate_height'] * aggregate_height
        )
        
        return score
    
    def _count_completed_lines(self, board):
        """Count the number of completed lines on the board"""
        completed = 0
        for row in range(BOARD_HEIGHT):
            if all(board[row]):
                completed += 1
        return completed
    
    def _get_column_heights(self, board):
        """Get the height of each column (highest occupied cell)"""
        heights = [0] * BOARD_WIDTH
        for col in range(BOARD_WIDTH):
            for row in range(BOARD_HEIGHT):
                if board[row][col]:
                    heights[col] = BOARD_HEIGHT - row
                    break
        return heights
    
    def _get_bumpiness(self, heights):
        """Calculate the sum of height differences between adjacent columns"""
        bumpiness = 0
        for i in range(len(heights) - 1):
            bumpiness += abs(heights[i] - heights[i + 1])
        return bumpiness
    
    def _count_holes(self, board, heights):
        """Count holes (empty cells with at least one filled cell above)"""
        holes = 0
        for col in range(BOARD_WIDTH):
            # Skip if column is empty
            if heights[col] == 0:
                continue
            
            # Count empty cells below the highest filled cell
            for row in range(BOARD_HEIGHT - heights[col], BOARD_HEIGHT):
                if not board[row][col]:
                    holes += 1
        
        return holes