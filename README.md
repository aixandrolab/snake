# Old Snake Game - Classic Arcade Game <sup>v1.0.0</sup>

[![GitHub top language](https://img.shields.io/github/languages/top/aixandrolab/snake)](https://github.com/aixandrolab/snake)
[![GitHub license](https://img.shields.io/github/license/aixandrolab/snake)](https://github.com/aixandrolab/snake/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/aixandrolab/snake)](https://github.com/aixandrolab/snake/)
[![GitHub stars](https://img.shields.io/github/stars/aixandrolab/snake?style=social)](https://github.com/aixandrolab/snake/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/aixandrolab/snake?style=social)](https://github.com/aixandrolab/snake/network/members)


A modern, visually enhanced remake of the classic Snake arcade game built with Python and Pygame. Features smooth controls, beautiful graphics, sound effects, and a persistent leaderboard system.

![Gameplay Screenshot](https://github.com/aixandrolab/snake/blob/master/data/images/playground.png)

## 🎮 Features

- **Classic Snake Gameplay** - Control a snake that grows longer as it eats food
- **Modern Graphics** - Gradient backgrounds, animated food, detailed snake design with eyes
- **Customizable Settings** - Adjust game speed (10-30 FPS) and snake color (6 options)
- **Leaderboard System** - Persistent SQLite database tracking top 5 high scores
- **Sound Effects** - Background music, button clicks, and eating sounds
- **Responsive UI** - Interactive buttons with hover effects and visual feedback
- **Pause Functionality** - Press SPACE to pause/resume the game

## 🖥️ Screenshots

| Main Menu                                                                                  | Leaderboard                                                                                  | Gameplay                                                                                 |
|--------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| ![Main Menu](https://github.com/aixandrolab/snake/blob/master/data/images/main_screen.png) | ![Leaderboard](https://github.com/aixandrolab/snake/blob/master/data/images/leaderboard.png) | ![Gameplay](https://github.com/aixandrolab/snake/blob/master/data/images/playground.png) |

## 🎯 Game Controls

| Action       | Keys                          |
|--------------|-------------------------------|
| Move Left    | `←` or `A`                    |
| Move Right   | `→` or `D`                    |
| Move Up      | `↑` or `W`                    |
| Move Down    | `↓` or `S`                    |
| Pause/Resume | `SPACE`                       |
| Submit Score | `ENTER` (on Game Over screen) |

## 📋 Requirements

- Python 3.8 or higher
- Pygame library

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/aixandrolab/snake-game.git
cd snake-game
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install pygame-ce
```

### 3. Run the game

```bash
python app.py
```

## 📁 Project Structure

```
snake-game/
├── app.py                 # Application entry point
├── core/
│   ├── game.py           # Main game logic and state management
│   ├── models/           # Game entity models
│   │   ├── button.py     # UI button component
│   │   ├── food.py       # Food/Apple entity with animation
│   │   ├── input_box.py  # Text input component
│   │   └── snake.py      # Snake entity with collision detection
│   └── utils/            # Utility modules
│       ├── colors.py     # Color palette definitions
│       ├── direction.py  # Movement direction enum
│       └── position.py   # Position dataclass
├── tools/
│   └── database.py       # SQLite leaderboard management
├── data/                 # Game assets
│   ├── images/
│   │   ├── leaderboard.png    # Leaderboard image
│   │   ├── main_screen.png    # Main screen image
│   │   ├── playground.png     # Playground image
│   │   └── snake.png     # Background image
│   ├── music/
│   │   ├── music.mp3     # Background music
│   │   └── game_over.mp3 # Game over music
│   └── sounds/
│       ├── button.wav    # Button click sound
│       └── eat.wav       # Food eating sound
└── requirements.txt      # Python dependencies
```

## 🎨 Game Features in Detail

### Snake Design
- Gradient-colored segments (head is brighter)
- Detailed eyes with pupils and highlights
- Directional eye positioning
- Smooth rounded corners

### Food Animation
- Pulsing glow effect
- Apple shape with leaf detail
- Responsive collision detection

### Visual Effects
- Gradient background with subtle grid overlay
- Button hover and click animations
- Text shadows for better readability
- Dark overlay for menu screens

## 💾 Leaderboard System

Scores are stored in an SQLite database (`snake_game.db`):

- Only the highest score per nickname is saved
- Top 5 scores are displayed in the leaderboard

## 🎵 Sound Effects

The game includes:
- Background music during menu and gameplay
- Eating sound when food is consumed
- Button click feedback
- Game over music

*Note: The game will run without sound files if they're missing.*

## 🔧 Customization

### Change Game Window Size

Edit `core/game.py`:

```python
self.width = 1000  # Your preferred width
self.height = 700  # Your preferred height
```

### Modify Game Speed Options

In `draw_settings_screen()` method:

```python
speeds = [10, 15, 20, 25, 30]  # Add or remove speed options
```

### Add New Snake Colors

In `core/utils/colors.py`:

```python
SNAKE_YOUR_COLOR = (R, G, B)  # Add to Colors class
```

Then add to the colors list in `draw_settings_screen()`.

## 🚀 Building Executable

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "data:data" app.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👤 Author

**Alexander Suvorov**

- GitHub: [@aixandrolab](https://github.com/aixandrolab)
- Project Link: [https://github.com/aixandrolab/snake-game](https://github.com/aixandrolab/snake-game)

## 🙏 Acknowledgments

- Inspired by the classic Nokia Snake game
- Built with Python and Pygame community tools
- Sound effects and music from free sources

## ⭐ Show your support

Give a ⭐️ if this project helped you!

---

## 📖 How to Play

1. Launch the game using `python app.py`
2. Click "START GAME" to begin
3. Control the snake to eat red apples
4. Each apple increases your score and snake length
5. Avoid hitting walls or your own tail
6. Press SPACE to pause if needed
7. After game over, enter your nickname to save your score
8. Check the leaderboard to see top players

## 🐛 Troubleshooting

| Issue            | Solution                                          |
|------------------|---------------------------------------------------|
| Game won't start | Ensure Python 3.8+ and Pygame are installed       |
| No sound         | Check that sound files exist in `data/` directory |
| Black screen     | Verify graphics drivers are up to date            |
| Database error   | Ensure write permissions in game directory        |

---

*Happy gaming! 🐍*
