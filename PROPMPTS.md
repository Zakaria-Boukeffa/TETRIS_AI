# AI Prompt Documentation

This document contains the prompts used during the development of the Tetris: Human vs AI game project.

## Initial Development Prompt

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

```
continue
```



