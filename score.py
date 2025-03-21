"""
Score management for the Tetris game.
Handles score calculation and tracking for both players.
"""

from constants import (
    POINTS_PER_LINE, BONUS_2_LINES, BONUS_3_LINES, 
    BONUS_4_LINES, SPECIAL_PIECE_BONUS
)

class ScoreManager:
    def __init__(self):
        """Initialize the score manager with zero scores for both players"""
        self.human_score = 0
        self.ai_score = 0
        self.human_special_piece_active = False
        self.ai_special_piece_active = False
    
    def reset_scores(self):
        """Reset both player scores to zero"""
        self.human_score = 0
        self.ai_score = 0
        self.human_special_piece_active = False
        self.ai_special_piece_active = False
    
    def get_human_score(self):
        """Get the current human player score"""
        return self.human_score
    
    def get_ai_score(self):
        """Get the current AI player score"""
        return self.ai_score
    
    def update_human_score(self, lines_cleared):
        """
        Update the human player's score based on lines cleared
        Returns the number of points added
        """
        return self._update_score(lines_cleared, True)
    
    def update_ai_score(self, lines_cleared):
        """
        Update the AI player's score based on lines cleared
        Returns the number of points added
        """
        return self._update_score(lines_cleared, False)
    
    def _update_score(self, lines_cleared, is_human):
        """
        Update a player's score based on lines cleared and apply bonuses
        Returns the number of points added
        """
        points = 0
        
        # Base points for clearing lines
        if lines_cleared > 0:
            points += lines_cleared * POINTS_PER_LINE
        
        # Bonus points for multiple lines
        if lines_cleared == 2:
            points += BONUS_2_LINES
        elif lines_cleared == 3:
            points += BONUS_3_LINES
        elif lines_cleared == 4:
            points += BONUS_4_LINES
        
        # Apply special piece bonus if applicable
        if is_human and self.human_special_piece_active:
            points += SPECIAL_PIECE_BONUS
            self.human_special_piece_active = False
        elif not is_human and self.ai_special_piece_active:
            points += SPECIAL_PIECE_BONUS
            self.ai_special_piece_active = False
        
        # Update the appropriate score
        if is_human:
            self.human_score += points
        else:
            self.ai_score += points
        
        return points
    
    def activate_special_piece_bonus(self, is_human):
        """Activate the special piece bonus for a player"""
        if is_human:
            self.human_special_piece_active = True
        else:
            self.ai_special_piece_active = True