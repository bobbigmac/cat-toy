# Cat Toy

An interactive pygame application designed to entertain cats with moving shapes, natural colors, and twitchy movements.

## Features

- **Natural Color Palette**: Earth tones, forest greens, and warm browns that appeal to cats
- **Dynamic Shapes**: Circles, squares, triangles, and stars that move around the screen
- **Smart Twitching**: Shapes occasionally twitch with debounced cooldowns to avoid constant movement
- **Interactive**: Keypresses trigger random actions like adding/removing shapes, changing colors, and forcing twitches
- **Cat-Friendly**: Larger shapes (50-120 pixels) with smooth movement and occasional surprises

## Requirements

- Python 3.x
- pygame

## Installation

1. Clone the repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install pygame`

## Usage

Run the application:
```bash
python cat-toy.py
```

### Controls

- **Any key**: Trigger random actions (add/remove shapes, change colors, force twitches)
- **Ctrl + Shift + W**: Exit the application

## How It Works

The application creates a fullscreen display with moving shapes that:
- Move smoothly across the screen
- Change size dynamically based on movement
- Occasionally twitch with controlled randomness
- Respond to user interaction with more activity
- Use natural, cat-friendly colors

Perfect for keeping cats entertained and engaged!
