# Wordle Solver

Hey peeps! This is a Python-based solver for [Wordle](https://www.nytimes.com/games/wordle/index.html).  
Given feedback from each guess, it suggests the optimal next word, and it’ll even start you off with high-vowel words to narrow down solutions fast.

---

## Features

- **Interactive CLI**:  
  - Enter your guess and its feedback (`g`=green, `y`=yellow, `b`=black)  
  - Example: Guess `AUREI` and get feedback _yellow/black/black/black/green_ ⇒ enter `ybbbg`  
- **Custom word list**: Uses `words.txt` by default—swap in your own 5-letter word list anytime.  
- **Pure Python**: No dependencies beyond the standard library.

---

## Prerequisites

- Python **3.8+** (3.13.4 works great)  
- A terminal (Command Prompt, PowerShell, Bash, etc.)

---

## Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/DiTakCoder/Wordle-Solver.git
   cd Wordle-Solver

*Have Fun! :)*
