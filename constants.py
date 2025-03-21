"""
Constants for the Tetris game.
This file contains configuration parameters used throughout the game.
"""

# Window Dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
BACKGROUND_COLOR = "#2C3E50"

# Board Dimensions
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE = 25

# Game Speeds
INITIAL_SPEED = 400  # milliseconds between piece movements
SPEED_INCREASE = 100   # speed increase per level (ms)
MIN_SPEED = 100       # minimum speed (ms)

# Board Positions
HUMAN_BOARD_X = 50
AI_BOARD_X = 450
BOARD_Y = 50

# Colors
GRID_COLOR = "#34495E"
BORDER_COLOR = "#ECF0F1"
TEXT_COLOR = "#ECF0F1"
BONUS_TEXT_COLOR = "#F1C40F"

# Piece Colors
PIECE_COLORS = {
    'I': "#1ABC9C",  # Cyan
    'J': "#3498DB",  # Blue
    'L': "#F39C12",  # Orange
    'O': "#F1C40F",  # Yellow
    'S': "#2ECC71",  # Green
    'T': "#9B59B6",  # Purple
    'Z': "#E74C3C",  # Red
    'SPECIAL': "#FF00FF"  # Magenta for special pieces
}

# Alternative colors for color change feature
ALT_PIECE_COLORS = {
    'I': "#E74C3C",  # Red
    'J': "#F1C40F",  # Yellow
    'L': "#2ECC71",  # Green
    'O': "#3498DB",  # Blue
    'S': "#9B59B6",  # Purple
    'T': "#1ABC9C",  # Cyan
    'Z': "#F39C12",  # Orange
    'SPECIAL': "#00FFFF"  # Cyan for special pieces
}

# Scoring
POINTS_PER_LINE = 50
BONUS_2_LINES = 100
BONUS_3_LINES = 200
BONUS_4_LINES = 300
SPECIAL_PIECE_BONUS = 100

# Special rule thresholds
SLOWDOWN_BONUS_THRESHOLD = 1000
SLOWDOWN_BONUS_DURATION = 10000  # 10 seconds in milliseconds
SLOWDOWN_PERCENTAGE = 0.8  # 20% slower
SPECIAL_PIECE_THRESHOLD = 3000
COLOR_CHANGE_INTERVAL = 120000  # 2 minutes in milliseconds
COLOR_CHANGE_DURATION = 20000   # 20 seconds in milliseconds


# Tetromino Shapes (representing the 7 standard tetrominos)
SHAPES = {
    'I': [
        [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
    ],
    'J': [
        [[1, 0, 0],
         [1, 1, 1],
         [0, 0, 0]],
    ],
    'L': [
        [[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]],
    ],
    'O': [
        [[1, 1],
         [1, 1]],
    ],
    'S': [
        [[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]],
    ],
    'T': [
        [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]],
    ],
    'Z': [
        [[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]],
    ],
    'SPECIAL': [
        # Star-shaped special piece
        [[0, 1, 0, 0, 0],
         [0, 0, 1, 0, 0],
         [1, 1, 1, 1, 1],
         [0, 0, 1, 0, 0],
         [0, 1, 0, 0, 0]],
    ]
}

# AI Settings
AI_MOVE_DELAY = 100  # milliseconds between AI moves
AI_THINKING_DEPTH = 2  # how many moves ahead AI considers