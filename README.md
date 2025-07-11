# Rubik's Cube Visualizer

A Flask web application for visualizing and interacting with a Rubik's cube.

## Features

- Interactive Rubik's cube visualization
- Move buttons for all 12 basic moves (U, D, L, R, F, B and their primes)
- Keyboard shortcuts (U/D/L/R/F/B for clockwise, Shift+U/D/L/R/F/B for counterclockwise)
- Mix cube functionality (applies 20 random moves)
- Reset functionality
- Support for both colored and test cubes
- Responsive web interface

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

- **Move Buttons**: Click the move buttons in the sidebar to rotate the cube
- **Keyboard Shortcuts**: 
  - Press U/D/L/R/F/B for clockwise moves
  - Press Shift+U/D/L/R/F/B for counterclockwise moves
- **Mix Cube**: Click the "Mix Cube" button to apply 20 random moves
- **Reset**: Click "Reset Cube" to return to the solved state
- **Cube Type**: Select between "Standard Cube" (colored) and "Test Cube" (letters/numbers)

## Project Structure

- `app.py` - Main Flask application
- `cube.py` - Core Rubik's cube logic and operations
- `templates/index.html` - HTML template for the web interface
- `requirements.txt` - Python dependencies

## API Endpoints

- `GET /` - Main page with cube visualization
- `POST /move` - Apply a move to the cube
- `POST /mix` - Mix the cube with random moves
- `POST /reset` - Reset the cube to solved state

## Technologies Used

- **Backend**: Flask, NumPy
- **Frontend**: HTML, CSS, JavaScript, jQuery
- **Cube Logic**: Custom NumPy-based implementation 