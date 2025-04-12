# Photonic Ship

Photonic Ship is a simple 2D game made in Python using Pygame. It was developed for a project at Vilnius University on April 12, 2025. The game includes basic mechanics inspired by quantum computing concepts like state switching and measurement.

## How to Play

You control a green spaceship and try to avoid red enemies. The game includes two modes:

- **Classic mode**: You play in either the top or bottom half of the screen (`|0⟩` or `|1⟩`).
- **Quantum mode**: You control two ships at once (superposition) with a chance-based outcome when hit.

If your ship collides with an enemy, a measurement is made. Depending on the result, you either survive or the game ends.

## Controls

- Arrow keys: Move the ship
- `H`: Switch between classic and quantum mode
- `X`: Flip classic state between `|0⟩` and `|1⟩`
- `Z`: Flip quantum state between `|+⟩` and `|-⟩`
- `F`: Freeze enemies temporarily
- `R`: Teleport the ship to a random location
- `ESC`: Quit the game

## Requirements

- Python3
- Pygame

If Pygame is not installed, it will be installed automatically when the game starts.

## How to Run

```bash
python quantum_ship.py
