# AI Prompt Documentation

This document contains the prompts used during the development of the Tetris: Human vs AI game project.

## prompt used to create the best prompts : GPT-4o
```
Using the details from the 'prompt' file and the 'tetris_project' file, generate the most effective prompt to instruct a generative AI to develop the project for me. 
Note: The 'prompt' file serves as a guide for creating a good prompt, while the 'tetris_project' file is a test for a course on using generative AI for code generation.
```

## Initial Development Prompt : Claude

```
- Goal:
Develop a two-player Tetris game (Human vs. AI) using Python and Tkinter, following the given specifications.
- Return Format:
The AI should generate a fully functional, well-structured, and well-documented Python project, including:
1. Complete Source Code
Implemented in Python using Tkinter for the graphical interface.
Organized in multiple files/modules for better readability (e.g., main.py, tetris.py, ai.py, score.py, constants.py).
Code must follow clean coding practices (clear variable names, comments, and function-based structure).
Ensure smooth execution with no major bugs.
2. README.md (Project Documentation)
Project Description: Brief explanation of the game and its features.
Installation Instructions: Steps to install dependencies and run the game.
How to Play: Explanation of controls for both human and AI players.
Special Rules: Description of fun mechanics (Surprise Gift, Slowdown Bonus, Special Piece, Color Change).
Technical Details: Overview of the code structure and how each module works.
3. PROMPTS.md (AI Prompt Documentation)
List of all prompts used during the development of the project.
- Requirements:
1. Game Structure:
Two grids: one for the human player and one for the AI.
Side-by-side display.
2. Controls:
Human Player: Uses arrow keys (← for left, → for right, ↓ for soft drop, ↑ for rotation).
AI Player: Plays automatically with a simple logic to place pieces efficiently.
3. Scoring System:
50 points per cleared line.
Bonus points: 100 for 2 lines, 200 for 3 lines, 300 for 4 lines (Tetris).
Live score display for both players.
4. Special Rules for Fun Gameplay:
Surprise Gift: Clearing 2 lines grants the opponent an easy piece (e.g., square or straight line).
Slowdown Bonus: Every 1000 points, pieces fall 20% slower for 10 seconds.
Special Piece: Every 3000 points, a unique-shaped piece appears (e.g., heart or star), awarding 100 bonus points if placed correctly.
Color Change: Every 2 minutes, piece colors change for 20 seconds (purely visual).
5. Evaluation Criteria (20 points total):
Prompt Quality (10 points) – effectiveness, creativity, and documentation.
Functionality (7 points) – proper implementation of game mechanics.
Documentation & Usability (3 points) – clarity of instructions and code structure.
- Warnings:
1. Ensure all rules and special mechanics (Surprise Gift, Slowdown Bonus, Special Piece, Color Change) are implemented exactly as described.
2.The AI should play logically but not too perfectly.
3.The game must be visually appealing and bug-free.
- Context Dump:
This project is part of a course on Generative AI for Code Generation. The course focuses on teaching how to use AI tools to generate functional code for specific tasks.
```

## Continuation Prompt

- I had a problem with the ui, So I asked 

```
Fix this issue: The text at the bottom of the window is not showing properly. The score of both players and the instructions section are overlapping, making it difficult to read. It seems like the window is not big enough, or the layout is not handling the text correctly
```

- Timer Placement:

```
Create a timer in the middle of the screen. It should be clearly visible and properly positioned without overlapping other elements.
```

- Score Calculation Fix:
```
There's a problem with the scoring—it sometimes gives incorrect calculations. Fix it by applying this exact logic:
Points:
50 par ligne.
Bonus: 100 pour 2 lignes, 200 pour 3 lignes, 300 pour un Tetris (4 lignes).
Affiche les scores en direct pour les deux joueurs.
```

- PS: I only had the free version of Claude, so once I reached the limit, I switched to Perplexity. I uploaded all the files and continued developing.

## Final Prompt
```
Find attached the project files. Check if the following functions were correctly implemented:  

Core Features  
- Two grids:  
  - One for the human player.  
  - One for the AI, displayed side by side.  

- Controls:  
  - Human: Arrow keys (left, right, down, up to rotate).  
  - AI: Plays automatically using simple logic (e.g., placing pieces optimally without complex decision-making).  

- Scoreboard:  
  - Points:  
    - 50 points per cleared line.  
    - Bonus:  
      - 100 for 2 lines.  
      - 200 for 3 lines.  
      - 300 for a Tetris (4 lines).  
  - Displays live scores for both players.  

Fun Rules  
1. Surprise Gift  
   - When a player clears 2 lines at once, the opponent receives an "easy piece" (e.g., a square or a straight line) to help them.  

2. Soft Pause  
   - Every 1,000 points, piece fall speed decreases by 20% for 10 seconds, giving both players a short break.  

3. Funny Piece
   - Every 3,000 points, a special piece (e.g., heart or star) appears. If placed correctly, it grants a 100-point bonus.  

4. Rainbow Mode  
   - Every 2 minutes, pieces change color for 20 seconds—purely visual fun, no gameplay impact.  
```
